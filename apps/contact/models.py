from django.db import models
from apps.common.models import BaseModel


class ContactMessage(BaseModel):
    """
    Mensajes de contacto general (no relacionados con adopciones)
    """
    
    SUBJECT_CHOICES = [
        ('general', 'Consulta general'),
        ('volunteer', 'Quiero ser voluntario'),
        ('donation', 'Donaciones'),
        ('found_pet', 'Encontré una mascota'),
        ('lost_pet', 'Perdí mi mascota'),
        ('other', 'Otro'),
    ]
    
    STATUS_CHOICES = [
        ('new', 'Nuevo'),
        ('in_progress', 'En proceso'),
        ('resolved', 'Resuelto'),
        ('closed', 'Cerrado'),
    ]
    
    # Datos del contacto
    full_name = models.CharField(
        max_length=100,
        verbose_name='Nombre completo'
    )
    email = models.EmailField(
        verbose_name='Correo electrónico'
    )
    phone = models.CharField(
        max_length=15,
        verbose_name='Teléfono',
        blank=True
    )
    
    # Mensaje
    subject = models.CharField(
        max_length=20,
        choices=SUBJECT_CHOICES,
        verbose_name='Asunto'
    )
    message = models.TextField(
        verbose_name='Mensaje'
    )
    
    # Estado
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Estado'
    )
    
    # Respuesta del admin
    admin_response = models.TextField(
        verbose_name='Respuesta del administrador',
        blank=True
    )
    responded_by = models.ForeignKey(
        'authentication.AdminUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Respondido por'
    )
    response_date = models.DateTimeField(
        verbose_name='Fecha de respuesta',
        null=True,
        blank=True
    )
    
    class Meta:
        verbose_name = 'Mensaje de contacto'
        verbose_name_plural = 'Mensajes de contacto'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.full_name} - {self.get_subject_display()}"