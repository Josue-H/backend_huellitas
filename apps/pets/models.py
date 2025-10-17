from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.common.models import BaseModel


class Pet(BaseModel):
    """
    Modelo para las mascotas disponibles para adopción
    """
    
    # Choices
    GENDER_CHOICES = [
        ('M', 'Macho'),
        ('F', 'Hembra'),
    ]
    
    SIZE_CHOICES = [
        ('small', 'Pequeño'),
        ('medium', 'Mediano'),
        ('large', 'Grande'),
        ('extra_large', 'Extra Grande'),
    ]
    
    STATUS_CHOICES = [
        ('available', 'Disponible'),
        ('adopted', 'Adoptado'),
        ('in_process', 'En proceso de adopción'),
        ('not_available', 'No disponible'),
    ]
    
    SPECIES_CHOICES = [
        ('dog', 'Perro'),
        ('cat', 'Gato'),
        ('other', 'Otro'),
    ]
    
    # Campos básicos
    name = models.CharField(
        max_length=100,
        verbose_name='Nombre'
    )
    species = models.CharField(
        max_length=20,
        choices=SPECIES_CHOICES,
        default='dog',
        verbose_name='Especie'
    )
    breed = models.CharField(
        max_length=100,
        verbose_name='Raza',
        blank=True
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        verbose_name='Sexo'
    )
    age_years = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(25)],
        verbose_name='Edad (años)',
        default=0
    )
    age_months = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(11)],
        verbose_name='Edad (meses)',
        default=0
    )
    size = models.CharField(
        max_length=20,
        choices=SIZE_CHOICES,
        verbose_name='Tamaño'
    )
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Peso (kg)',
        blank=True,
        null=True
    )
    color = models.CharField(
        max_length=100,
        verbose_name='Color',
        blank=True
    )
    
    # Estado y salud
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available',
        verbose_name='Estado'
    )
    is_sterilized = models.BooleanField(
        default=False,
        verbose_name='Castrado/Esterilizado'
    )
    is_vaccinated = models.BooleanField(
        default=False,
        verbose_name='Vacunado'
    )
    is_dewormed = models.BooleanField(
        default=False,
        verbose_name='Desparasitado'
    )
    
    # Descripción y características
    description = models.TextField(
        verbose_name='Sobre mí',
        help_text='Descripción corta sobre la mascota',
        blank=True
    )
    characteristics = models.TextField(
        verbose_name='Características especiales',
        help_text='Temperamento, personalidad, necesidades especiales, etc.',
        blank=True
    )
    special_needs = models.TextField(
        verbose_name='Necesidades especiales',
        blank=True
    )
    
    # Características adicionales para adopción
    friendly_with_kids = models.BooleanField(
        default=False,
        verbose_name='Amigable con niños'
    )
    adapts_to_indoor_living = models.BooleanField(
        default=True,
        verbose_name='Se adapta a vivir dentro de casa'
    )
    easy_to_train = models.BooleanField(
        default=False,
        verbose_name='Fácil de entrenar'
    )
    
    ENERGY_LEVEL_CHOICES = [
        ('low', 'Bajo'),
        ('medium', 'Medio'),
        ('high', 'Alto'),
    ]
    
    energy_level = models.CharField(
        max_length=10,
        choices=ENERGY_LEVEL_CHOICES,
        default='medium',
        verbose_name='Nivel de energía'
    )
    
    # Fechas importantes
    arrival_date = models.DateField(
        verbose_name='Fecha de llegada',
        auto_now_add=True
    )
    adoption_date = models.DateField(
        verbose_name='Fecha de adopción',
        blank=True,
        null=True
    )
    
    # Imágenes
    main_image = models.ImageField(
        upload_to='pets/main/',
        verbose_name='Imagen principal',
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name = 'Mascota'
        verbose_name_plural = 'Mascotas'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.get_species_display()})"
    
    @property
    def age_display(self):
        """Retorna la edad en formato legible"""
        if self.age_years > 0 and self.age_months > 0:
            return f"{self.age_years} años, {self.age_months} meses"
        elif self.age_years > 0:
            return f"{self.age_years} años"
        else:
            return f"{self.age_months} meses"
    
    @property
    def is_available(self):
        """Verifica si la mascota está disponible para adopción"""
        return self.status == 'available' and self.is_active


class PetImage(BaseModel):
    """
    Imágenes adicionales de las mascotas
    """
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Mascota'
    )
    image = models.ImageField(
        upload_to='pets/gallery/',
        verbose_name='Imagen'
    )
    caption = models.CharField(
        max_length=200,
        verbose_name='Descripción',
        blank=True
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Orden'
    )
    
    class Meta:
        verbose_name = 'Imagen de mascota'
        verbose_name_plural = 'Imágenes de mascotas'
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"Imagen de {self.pet.name}"