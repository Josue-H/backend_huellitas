from django.urls import path
from .views import (
    admin_login,
    admin_logout,
    current_admin_user,
    update_admin_profile,
    change_password,
    AdminActivityLogListView
)

app_name = 'authentication'

urlpatterns = [
    # Autenticación
    path('login/', admin_login, name='admin-login'),
    path('logout/', admin_logout, name='admin-logout'),
    path('me/', current_admin_user, name='current-user'),
    
    # Perfil
    path('profile/', update_admin_profile, name='update-profile'),
    path('change-password/', change_password, name='change-password'),
    
    # Logs de actividad
    path('activity-logs/', AdminActivityLogListView.as_view(), name='activity-logs'),
]