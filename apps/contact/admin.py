from django.contrib import admin
from django.utils.html import format_html
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """
    Administración de mensajes de contacto
    """
    list_display = [
        'id', 
        'full_name_link',  # CAMBIO: Hacer el nombre clickeable
        'email', 
        'phone',
        'subject_display',
        'status_display',
        'created_at'
    ]
    
    list_display_links = ['id', 'full_name_link']  # IMPORTANTE: Hacer clickeables
    
    list_filter = [
        'status', 
        'subject', 
        'created_at'
    ]
    
    search_fields = [
        'full_name', 
        'email', 
        'phone', 
        'message'
    ]
    
    readonly_fields = [
        'id',
        'full_name', 
        'email', 
        'phone', 
        'subject',
        'subject_display',
        'message', 
        'created_at', 
        'updated_at'
    ]
    
    # Vista de detalle organizada
    fieldsets = (
        ('Información del Contacto', {
            'fields': (
                'id',
                'full_name',
                'email',
                'phone',
            )
        }),
        ('Mensaje', {
            'fields': (
                'subject',
                'message',
                'created_at',
                'updated_at'
            )
        }),
        ('Gestión Administrativa', {
            'fields': (
                'status',
                'admin_response',
            ),
            'classes': ('collapse',)  # Colapsable por defecto
        }),
    )
    
    list_per_page = 25
    
    # Acciones personalizadas
    actions = ['mark_as_in_progress', 'mark_as_resolved', 'mark_as_closed']
    
    def full_name_link(self, obj):
        """Mostrar el nombre como enlace clickeable"""
        return obj.full_name
    full_name_link.short_description = 'Nombre Completo'
    
    def subject_display(self, obj):
        """Mostrar el asunto en formato legible"""
        return obj.get_subject_display()
    subject_display.short_description = 'Asunto'
    
    def status_display(self, obj):
        """Mostrar el estado en formato legible con colores"""
        colors = {
            'new': '#28a745',       # Verde
            'in_progress': '#ffc107',  # Amarillo
            'resolved': '#17a2b8',  # Azul
            'closed': '#6c757d'     # Gris
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="color: {}; font-weight: bold;">●</span> {}',
            color,
            obj.get_status_display()
        )
    status_display.short_description = 'Estado'
    
    # Acciones rápidas para cambiar estado
    @admin.action(description='Marcar como "En proceso"')
    def mark_as_in_progress(self, request, queryset):
        updated = queryset.update(status='in_progress')
        self.message_user(request, f'{updated} mensaje(s) marcado(s) como "En proceso".')
    
    @admin.action(description='Marcar como "Resuelto"')
    def mark_as_resolved(self, request, queryset):
        updated = queryset.update(status='resolved')
        self.message_user(request, f'{updated} mensaje(s) marcado(s) como "Resuelto".')
    
    @admin.action(description='Marcar como "Cerrado"')
    def mark_as_closed(self, request, queryset):
        updated = queryset.update(status='closed')
        self.message_user(request, f'{updated} mensaje(s) marcado(s) como "Cerrado".')
    
    def has_add_permission(self, request):
        """Los mensajes solo se crean desde el frontend"""
        return False