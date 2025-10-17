from django.db import models
from django.core.validators import RegexValidator


class StatusChoices(models.TextChoices):
    """
    Opciones de estado para diferentes modelos
    """
    ACTIVE = 'active', 'Activo'
    INACTIVE = 'inactive', 'Inactivo'
    PENDING = 'pending', 'Pendiente'
    APPROVED = 'approved', 'Aprobado'
    REJECTED = 'rejected', 'Rechazado'


class TimestampedModel(models.Model):
    """
    Modelo abstracto que proporciona campos de fecha de creación y modificación
    """
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de modificación'
    )

    class Meta:
        abstract = True


class ActiveManager(models.Manager):
    """
    Manager que solo devuelve objetos activos
    """
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class BaseModel(TimestampedModel):
    """
    Modelo base para la mayoría de modelos de la aplicación
    """
    is_active = models.BooleanField(
        default=True,
        verbose_name='Activo'
    )
    
    # Managers
    objects = models.Manager()  # Manager por defecto
    active = ActiveManager()    # Solo objetos activos

    class Meta:
        abstract = True


class Address(BaseModel):
    """
    Modelo para direcciones que pueden ser reutilizadas
    """
    street = models.CharField(
        max_length=255,
        verbose_name='Dirección'
    )
    city = models.CharField(
        max_length=100,
        verbose_name='Ciudad',
        default='Ciudad de Guatemala'
    )
    department = models.CharField(
        max_length=100,
        verbose_name='Departamento',
        default='Guatemala'
    )
    postal_code = models.CharField(
        max_length=10,
        verbose_name='Código postal',
        blank=True
    )
    country = models.CharField(
        max_length=50,
        verbose_name='País',
        default='Guatemala'
    )

    class Meta:
        verbose_name = 'Dirección'
        verbose_name_plural = 'Direcciones'

    def __str__(self):
        return f"{self.street}, {self.city}"


class PhoneNumber(BaseModel):
    """
    Modelo para números de teléfono
    """
    phone_regex = RegexValidator(
        regex=r'^\+?502?[0-9]{8}$',
        message="Formato: '+50212345678' o '12345678'"
    )
    
    number = models.CharField(
        validators=[phone_regex],
        max_length=15,
        verbose_name='Número de teléfono'
    )
    is_primary = models.BooleanField(
        default=False,
        verbose_name='Teléfono principal'
    )
    
    class Meta:
        verbose_name = 'Teléfono'
        verbose_name_plural = 'Teléfonos'
    
    def __str__(self):
        return self.number


class SiteConfiguration(models.Model):
    """
    Configuración general del sitio
    """
    site_name = models.CharField(
        max_length=100,
        default='Huellitas',
        verbose_name='Nombre del sitio'
    )
    contact_email = models.EmailField(
        verbose_name='Email de contacto'
    )
    contact_phone = models.CharField(
        max_length=15,
        verbose_name='Teléfono de contacto'
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Dirección principal'
    )
    about_us = models.TextField(
        verbose_name='Acerca de nosotros',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Configuración del sitio'
        verbose_name_plural = 'Configuraciones del sitio'
    
    def __str__(self):
        return self.site_name
    
    def save(self, *args, **kwargs):
        # Solo permitir una configuración
        if not self.pk and SiteConfiguration.objects.exists():
            raise ValueError('Solo puede existir una configuración del sitio')
        super().save(*args, **kwargs)