from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AdminUser, AdminActivityLog


@admin.register(AdminUser)
class AdminUserAdmin(UserAdmin):
    """
    Configuración del admin para AdminUser
    """
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {
            'fields': ('phone', 'role', 'profile_picture', 'is_active_session', 'last_activity')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información adicional', {
            'fields': ('phone', 'role', 'email')
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'last_activity')
    list_filter = ('role', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    readonly_fields = ('last_activity',)


@admin.register(AdminActivityLog)
class AdminActivityLogAdmin(admin.ModelAdmin):
    """
    Configuración del admin para logs de actividad
    """
    list_display = ('user', 'action', 'created_at', 'ip_address')
    list_filter = ('action', 'created_at')
    search_fields = ('user__username', 'description')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'