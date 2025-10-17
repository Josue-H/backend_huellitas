from django.contrib import admin
from .models import NewsArticle, SuccessStory, FAQ


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_featured', 'published_date', 'is_active')
    list_filter = ('is_featured', 'is_active', 'published_date', 'author')
    search_fields = ('title', 'summary', 'content')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('published_date', 'preview_image')
    date_hierarchy = 'published_date'
    list_editable = ('is_featured', 'is_active')
    
    def preview_image(self, obj):
        if obj.featured_image:
            return f'<img src="{obj.featured_image.url}" width="300" />'
        return "Sin imagen"
    preview_image.short_description = 'Vista previa'
    preview_image.allow_tags = True
    
    fieldsets = (
        ('Contenido', {
            'fields': ('title', 'slug', 'summary', 'content')
        }),
        ('Imagen', {
            'fields': ('featured_image', 'preview_image')
        }),
        ('Configuración', {
            'fields': ('is_featured', 'is_active', 'author')
        }),
        ('Fechas', {
            'fields': ('published_date',),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es nuevo
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(SuccessStory)
class SuccessStoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'pet_name', 'adopter_name', 'is_featured', 'created_at', 'is_active')
    list_filter = ('is_featured', 'is_active', 'created_at')
    search_fields = ('title', 'pet_name', 'adopter_name', 'story')
    readonly_fields = ('created_at', 'updated_at', 'preview_before', 'preview_after')
    date_hierarchy = 'created_at'
    list_editable = ('is_featured', 'is_active')
    
    def preview_before(self, obj):
        if obj.before_image:
            return f'<img src="{obj.before_image.url}" width="150" />'
        return "Sin imagen"
    preview_before.short_description = 'Vista previa (Antes)'
    preview_before.allow_tags = True
    
    def preview_after(self, obj):
        if obj.after_image:
            return f'<img src="{obj.after_image.url}" width="150" />'
        return "Sin imagen"
    preview_after.short_description = 'Vista previa (Después)'
    preview_after.allow_tags = True
    
    fieldsets = (
        ('Información del Testimonio', {
            'fields': ('title', 'pet_name', 'adopter_name')
        }),
        ('Historia', {
            'fields': ('story',)
        }),
        ('Imágenes', {
            'fields': ('before_image', 'preview_before', 'after_image', 'preview_after')
        }),
        ('Configuración', {
            'fields': ('is_featured', 'is_active')
        }),
    )


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'order', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('question', 'answer')
    list_editable = ('order',)
    ordering = ('category', 'order')