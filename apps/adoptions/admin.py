from django.contrib import admin
from .models import AdoptionApplication, PersonalReference, SimplifiedAdoptionRequest


# OCULTAR el formulario completo del admin (comentado)
# Si en el futuro lo necesitas, descomenta estas líneas

# class PersonalReferenceInline(admin.TabularInline):
#     model = PersonalReference
#     extra = 0
#     min_num = 3
#     max_num = 3
#     fields = ('full_name', 'phone', 'relationship')


# @admin.register(AdoptionApplication)
# class AdoptionApplicationAdmin(admin.ModelAdmin):
#     """
#     Configuración del admin para solicitudes completas (OCULTO)
#     """
#     list_display = ('full_name', 'pet', 'application_status', 'created_at', 'reviewed_by')
#     # ... resto del código


@admin.register(SimplifiedAdoptionRequest)
class SimplifiedAdoptionRequestAdmin(admin.ModelAdmin):
    """
    Admin para solicitudes simplificadas (formulario PDF)
    
    """
    list_display = ('full_name', 'pet', 'pet_name_requested', 'phone', 'status', 'created_at', 'reviewed_by')
    list_filter = ('status', 'created_at', 'pet__species')
    search_fields = ('full_name', 'phone', 'email', 'pet__name', 'pet_name_requested')
    readonly_fields = ('created_at', 'updated_at', 'pdf_preview')
    date_hierarchy = 'created_at'
    list_editable = ('status',)
    
    def pdf_preview(self, obj):
        if obj.filled_form_pdf:
            return f'''
                <a href="{obj.filled_form_pdf.url}" target="_blank" class="button">
                    📄 Ver Formulario PDF
                </a>
                <br><br>
                <iframe src="{obj.filled_form_pdf.url}" width="100%" height="600px"></iframe>
            '''
        return "No se ha cargado formulario"
    pdf_preview.short_description = 'Formulario Cargado'
    pdf_preview.allow_tags = True
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('pet', 'full_name', 'pet_name_requested', 'phone', 'email'),
            'description': 'Datos básicos proporcionados por el solicitante'
        }),
        ('Formulario PDF', {
            'fields': ('filled_form_pdf', 'pdf_preview'),
            'description': 'Formulario completo firmado por el solicitante'
        }),
        ('Estado de la Solicitud', {
            'fields': ('status', 'admin_notes', 'reviewed_by', 'review_date')
        }),
        ('Fechas del Sistema', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if change and 'status' in form.changed_data:
            # Si se cambió el estado, registrar quién lo revisó
            obj.reviewed_by = request.user
            from django.utils import timezone
            obj.review_date = timezone.now()
        super().save_model(request, obj, form, change)


# Mantener solo PersonalReference por si se usa en el futuro
@admin.register(PersonalReference)
class PersonalReferenceAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'relationship', 'application')
    search_fields = ('full_name', 'application__full_name', 'phone')
    list_filter = ('relationship',)