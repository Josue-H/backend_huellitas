from django.contrib import admin
from .models import Address, PhoneNumber, SiteConfiguration


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('street', 'city', 'department', 'country', 'is_active')
    list_filter = ('city', 'department', 'country', 'is_active')
    search_fields = ('street', 'city')


@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ('number', 'is_primary', 'is_active', 'created_at')
    list_filter = ('is_primary', 'is_active')
    search_fields = ('number',)


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'contact_email', 'contact_phone', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    
    def has_add_permission(self, request):
        # Solo permitir una configuración
        return not SiteConfiguration.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # No permitir eliminar la configuración
        return False