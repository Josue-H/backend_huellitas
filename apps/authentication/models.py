from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.common.models import BaseModel, TimestampedModel


class AdminUser(AbstractUser):
    """
    Usuario administrador para el panel de gestión
    Los adoptantes NO tienen cuenta - solo llenan formularios
    """
    
    ROLE_CHOICES = [
        ('super_admin', 'Super Administrador'),
        ('admin', 'Administrador'),
        ('volunteer', 'Voluntario'),
        ('veterinarian', 'Veterinario'),
    ]
    
    phone = models.CharField(
        max_length=15,
        verbose_name='Teléfono',
        blank=True
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='volunteer',
        verbose_name='Rol'
    )
    profile_picture = models.ImageField(
        upload_to='admin_profiles/',
        verbose_name='Foto de perfil',
        blank=True,
        null=True
    )
    is_active_session = models.BooleanField(
        default=False,
        verbose_name='Sesión activa'
    )
    last_activity = models.DateTimeField(
        verbose_name='Última actividad',
        auto_now=True
    )
    
    # Solución para evitar conflictos con auth.User
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='admin_users',  # Cambiamos el related_name
        related_query_name='admin_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='admin_users',  # Cambiamos el related_name
        related_query_name='admin_user',
    )
    
    class Meta:
        verbose_name = 'Usuario Administrador'
        verbose_name_plural = 'Usuarios Administradores'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name else self.username
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username
    
    def has_permission(self, permission):
        """Verificar permisos según el rol"""
        permissions = {
            'super_admin': ['all'],
            'admin': ['pets', 'adoptions', 'content', 'users'],
            'volunteer': ['pets', 'adoptions'],
            'veterinarian': ['pets'],
        }
        user_permissions = permissions.get(self.role, [])
        return 'all' in user_permissions or permission in user_permissions


class AdminActivityLog(TimestampedModel):
    """
    Log de actividades de los administradores
    """
    
    ACTION_CHOICES = [
        ('login', 'Iniciar sesión'),
        ('logout', 'Cerrar sesión'),
        ('create_pet', 'Crear mascota'),
        ('update_pet', 'Actualizar mascota'),
        ('delete_pet', 'Eliminar mascota'),
        ('approve_adoption', 'Aprobar adopción'),
        ('reject_adoption', 'Rechazar adopción'),
        ('create_content', 'Crear contenido'),
        ('update_content', 'Actualizar contenido'),
    ]
    
    user = models.ForeignKey(
        AdminUser,
        on_delete=models.CASCADE,
        related_name='activity_logs',
        verbose_name='Usuario'
    )
    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES,
        verbose_name='Acción'
    )
    description = models.TextField(
        verbose_name='Descripción',
        blank=True
    )
    ip_address = models.GenericIPAddressField(
        verbose_name='Dirección IP',
        null=True,
        blank=True
    )
    
    class Meta:
        verbose_name = 'Log de actividad'
        verbose_name_plural = 'Logs de actividad'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_action_display()}"