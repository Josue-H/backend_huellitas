from django.db import models
from apps.common.models import BaseModel


class NewsArticle(BaseModel):
    """
    Artículos de noticias y novedades del refugio
    """
    title = models.CharField(
        max_length=200,
        verbose_name='Título'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='URL amigable'
    )
    summary = models.TextField(
        verbose_name='Resumen',
        max_length=300
    )
    content = models.TextField(
        verbose_name='Contenido'
    )
    featured_image = models.ImageField(
        upload_to='news/',
        verbose_name='Imagen destacada',
        blank=True,
        null=True
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name='Artículo destacado'
    )
    published_date = models.DateTimeField(
        verbose_name='Fecha de publicación',
        auto_now_add=True
    )
    author = models.ForeignKey(
        'authentication.AdminUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Autor'
    )
    
    class Meta:
        verbose_name = 'Artículo de noticias'
        verbose_name_plural = 'Artículos de noticias'
        ordering = ['-published_date']
    
    def __str__(self):
        return self.title


class SuccessStory(BaseModel):
    """
    Historias de éxito de adopciones
    """
    title = models.CharField(
        max_length=200,
        verbose_name='Título'
    )
    pet_name = models.CharField(
        max_length=100,
        verbose_name='Nombre de la mascota'
    )
    adopter_name = models.CharField(
        max_length=100,
        verbose_name='Nombre del adoptante',
        blank=True
    )
    story = models.TextField(
        verbose_name='Historia'
    )
    before_image = models.ImageField(
        upload_to='success_stories/before/',
        verbose_name='Imagen anterior',
        blank=True,
        null=True
    )
    after_image = models.ImageField(
        upload_to='success_stories/after/',
        verbose_name='Imagen actual',
        blank=True,
        null=True
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name='Historia destacada'
    )
    
    class Meta:
        verbose_name = 'Historia de éxito'
        verbose_name_plural = 'Historias de éxito'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.pet_name}"


class FAQ(BaseModel):
    """
    Preguntas frecuentes
    """
    question = models.CharField(
        max_length=200,
        verbose_name='Pregunta'
    )
    answer = models.TextField(
        verbose_name='Respuesta'
    )
    category = models.CharField(
        max_length=50,
        choices=[
            ('adoption', 'Adopción'),
            ('care', 'Cuidados'),
            ('donation', 'Donaciones'),
            ('volunteer', 'Voluntariado'),
            ('general', 'General'),
        ],
        verbose_name='Categoría'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Orden'
    )
    
    class Meta:
        verbose_name = 'Pregunta frecuente'
        verbose_name_plural = 'Preguntas frecuentes'
        ordering = ['category', 'order']
    
    def __str__(self):
        return self.question