from django.contrib import admin
from .models import Pet, PetImage


class PetImageInline(admin.TabularInline):
    model = PetImage
    extra = 1


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    """
    Configuración del admin para mascotas
    """
    list_display = ('name', 'species', 'breed', 'gender', 'age_display', 'status', 'is_active', 'created_at')
    list_filter = ('species', 'gender', 'status', 'size', 'is_sterilized', 'is_vaccinated', 'created_at')
    search_fields = ('name', 'breed', 'description')
    readonly_fields = ('created_at', 'updated_at', 'arrival_date', 'preview_image')
    date_hierarchy = 'created_at'
    inlines = [PetImageInline]
    list_editable = ('status', 'is_active')
    
    def preview_image(self, obj):
        if obj.main_image:
            return f'<img src="{obj.main_image.url}" width="200" />'
        return "Sin imagen"
    preview_image.short_description = 'Vista previa'
    preview_image.allow_tags = True
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'species', 'breed', 'gender', 'age_years', 'age_months')
        }),
        ('Características Físicas', {
            'fields': ('size', 'weight', 'color', 'main_image', 'preview_image')
        }),
        ('Estado y Salud', {
            'fields': ('status', 'is_sterilized', 'is_vaccinated', 'is_dewormed')
        }),
        ('Características para Adopción', {
            'fields': ('friendly_with_kids', 'adapts_to_indoor_living', 'easy_to_train', 'energy_level'),
            'classes': ('collapse',)
        }),
        ('Sobre mí', {
            'fields': ('description', 'characteristics', 'special_needs')
        }),
        ('Fechas', {
            'fields': ('arrival_date', 'adoption_date', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Estado del Registro', {
            'fields': ('is_active',),
            'classes': ('collapse',)
        }),
    )


@admin.register(PetImage)
class PetImageAdmin(admin.ModelAdmin):
    """
    Configuración del admin para imágenes de mascotas
    """
    list_display = ('pet', 'caption', 'order', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('pet__name', 'caption')