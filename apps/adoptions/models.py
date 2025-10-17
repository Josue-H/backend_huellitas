from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.common.models import BaseModel
from apps.pets.models import Pet


class AdoptionApplication(BaseModel):
    """
    Solicitud de adopción - Formulario público para solicitantes
    """
    
    # MASCOTA A ADOPTAR
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='adoption_applications',
        verbose_name='Mascota a adoptar'
    )
    
    # DATOS DEL SOLICITANTE
    full_name = models.CharField(
        max_length=200,
        verbose_name='Nombre completo'
    )
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(18), MaxValueValidator(100)],
        verbose_name='Edad'
    )
    civil_status = models.CharField(
        max_length=50,
        verbose_name='Estado civil',
        help_text='Soltero/a, Casado/a, Divorciado/a, Viudo/a, Unión libre'
    )
    profession = models.CharField(
        max_length=100,
        verbose_name='Profesión'
    )
    address = models.TextField(
        verbose_name='Dirección de domicilio'
    )
    home_phone = models.CharField(
        max_length=15,
        verbose_name='Teléfono de casa',
        blank=True
    )
    cell_phone = models.CharField(
        max_length=15,
        verbose_name='Celular'
    )
    email = models.EmailField(
        verbose_name='Correo electrónico'
    )
    
    # INFORMACIÓN DE VIVIENDA
    HOUSING_OWNERSHIP_CHOICES = [
        ('Propia', 'Propia'),
        ('Alquilada', 'Alquilada'),
    ]
    
    DWELLING_TYPE_CHOICES = [
        ('Casa', 'Casa'),
        ('Apartamento', 'Apartamento'),
        ('Finca', 'Finca'),
        ('Granja', 'Granja'),
    ]
    
    housing_ownership = models.CharField(
        max_length=20,
        choices=HOUSING_OWNERSHIP_CHOICES,
        verbose_name='¿Es casa propia o alquilada?'
    )
    landlord_permission = models.BooleanField(
        null=True,
        blank=True,
        verbose_name='¿El dueño está de acuerdo con mascotas?',
        help_text='Solo aplicable si la vivienda es alquilada'
    )
    dwelling_type = models.CharField(
        max_length=20,
        choices=DWELLING_TYPE_CHOICES,
        verbose_name='Tipo de vivienda'
    )
    
    # CUESTIONARIO SOBRE LA MASCOTA
    adoption_reason = models.TextField(
        verbose_name='¿Por qué desea adoptar? Explique'
    )
    pet_location_in_home = models.CharField(
        max_length=100,
        verbose_name='¿En dónde se mantendrá la mascota?',
        help_text='Ej: Patio, Jardín, Terraza, Toda la casa'
    )
    adults_in_home = models.PositiveIntegerField(
        verbose_name='¿Cuántos adultos viven en casa?'
    )
    children_in_home = models.PositiveIntegerField(
        default=0,
        verbose_name='¿Cuántos niños viven en casa?'
    )
    all_family_agrees = models.BooleanField(
        verbose_name='¿Todos aman a los animales y están de acuerdo?'
    )
    can_afford_pet = models.BooleanField(
        verbose_name='¿Tiene economía para alimentación, veterinario y gastos futuros?'
    )
    
    # EXPERIENCIA CON MASCOTAS
    has_had_pets_before = models.BooleanField(
        verbose_name='¿Alguna vez ha tenido mascota?'
    )
    previous_pet_experience = models.TextField(
        blank=True,
        verbose_name='¿Cuáles? ¿Qué les sucedió?',
        help_text='Describa su experiencia previa con mascotas'
    )
    has_current_pets = models.BooleanField(
        verbose_name='¿Tiene mascotas actualmente?'
    )
    current_pets_info = models.TextField(
        blank=True,
        verbose_name='Información de mascotas actuales',
        help_text='¿Cuántas y cuáles mascotas tiene?'
    )
    
    # PROPÓSITO Y EXPECTATIVAS
    ADOPTION_PURPOSE_CHOICES = [
        ('Para hogar', 'Para hogar'),
        ('Para guardianía', 'Para guardianía'),
    ]
    
    adoption_purpose = models.CharField(
        max_length=20,
        choices=ADOPTION_PURPOSE_CHOICES,
        verbose_name='¿Para hogar o guardianía?'
    )
    aware_of_potential_damage = models.BooleanField(
        verbose_name='¿Consciente de que puede dañar adornos?'
    )
    damage_plan = models.TextField(
        verbose_name='¿Qué haría ante posibles daños?'
    )
    willing_to_educate = models.BooleanField(
        verbose_name='¿Dispuesto a comprender y educar a la mascota?'
    )
    behavior_plan = models.TextField(
        verbose_name='¿Qué medidas tomaría si el comportamiento no es el esperado?'
    )
    
    # SEGUIMIENTO
    agrees_to_home_visits = models.BooleanField(
        verbose_name='¿Acepta visitas periódicas al domicilio?'
    )
    home_visit_reasoning = models.TextField(
        blank=True,
        verbose_name='¿Por qué?',
        help_text='Explique por qué acepta o no las visitas'
    )
    understands_no_transfer_policy = models.BooleanField(
        verbose_name='¿Comprende que no puede entregar a terceros?'
    )
    vision_in_5_years = models.TextField(
        verbose_name='¿Cómo se ve con su adoptado en 5 años?'
    )
    agrees_to_sterilize = models.BooleanField(
        verbose_name='¿Se compromete a esterilizar cuando tenga edad?'
    )
    
    # DOCUMENTOS ADJUNTOS
    dpi_copy = models.FileField(
        upload_to='adoptions/dpi/',
        verbose_name='Copia de DPI',
        help_text='Documento de identificación personal'
    )
    utility_bill_copy = models.FileField(
        upload_to='adoptions/bills/',
        verbose_name='Recibo de luz o teléfono',
        help_text='Comprobante de domicilio'
    )
    
    # ESTADO DE LA SOLICITUD
    APPLICATION_STATUS_CHOICES = [
        ('Recibida', 'Recibida'),
        ('En Revisión', 'En Revisión'),
        ('Aprobada', 'Aprobada'),
        ('Rechazada', 'Rechazada'),
    ]
    
    application_status = models.CharField(
        max_length=20,
        choices=APPLICATION_STATUS_CHOICES,
        default='Recibida',
        verbose_name='Estado de la solicitud'
    )
    
    # CAMPOS ADMINISTRATIVOS
    admin_notes = models.TextField(
        blank=True,
        verbose_name='Notas del administrador'
    )
    reviewed_by = models.ForeignKey(
        'authentication.AdminUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Revisado por',
        related_name='reviewed_applications'
    )
    review_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha de revisión'
    )
    
    class Meta:
        verbose_name = 'Solicitud de adopción'
        verbose_name_plural = 'Solicitudes de adopción'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.full_name} - {self.pet.name} ({self.application_status})"


class PersonalReference(models.Model):
    """
    Referencias personales del solicitante (3 referencias requeridas)
    """
    application = models.ForeignKey(
        AdoptionApplication,
        on_delete=models.CASCADE,
        related_name='references',
        verbose_name='Solicitud de adopción'
    )
    full_name = models.CharField(
        max_length=100,
        verbose_name='Nombre completo'
    )
    phone = models.CharField(
        max_length=15,
        verbose_name='Teléfono'
    )
    relationship = models.CharField(
        max_length=50,
        verbose_name='Parentesco o relación'
    )
    
    class Meta:
        verbose_name = 'Referencia personal'
        verbose_name_plural = 'Referencias personales'
    
    def __str__(self):
        return f"{self.full_name} - {self.application.full_name}"


class SimplifiedAdoptionRequest(BaseModel):
    """
    Solicitud simplificada de adopción (Frontend público)
    El usuario descarga el PDF, lo llena, firma y lo sube
    """
    
    STATUS_CHOICES = [
        ('Recibida', 'Recibida'),
        ('En Revisión', 'En Revisión'),
        ('Aprobada', 'Aprobada'),
        ('Rechazada', 'Rechazada'),
    ]
    
    # MASCOTA
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='simplified_applications',
        verbose_name='Mascota a adoptar'
    )
    
    # DATOS BÁSICOS DEL SOLICITANTE
    full_name = models.CharField(
        max_length=200,
        verbose_name='Nombre y apellido completo'
    )
    pet_name_requested = models.CharField(
        max_length=100,
        verbose_name='Nombre del perrito solicitado',
        help_text='Nombre de la mascota que desea adoptar'
    )
    phone = models.CharField(
        max_length=15,
        verbose_name='Número de teléfono (WhatsApp)'
    )
    email = models.EmailField(
        verbose_name='Correo electrónico',
        blank=True,
        null=True
    )
    
    # FORMULARIO PDF COMPLETO
    filled_form_pdf = models.FileField(
        upload_to='adoptions/simplified_forms/',
        verbose_name='Formulario de adopción completado y firmado (PDF)',
        help_text='Descargue el formulario, llénelo, fírmelo y súbalo escaneado'
    )
    
    # ESTADO
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Recibida',
        verbose_name='Estado de la solicitud'
    )
    
    # CAMPOS ADMINISTRATIVOS
    admin_notes = models.TextField(
        blank=True,
        verbose_name='Notas del administrador'
    )
    reviewed_by = models.ForeignKey(
        'authentication.AdminUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Revisado por',
        related_name='simplified_applications_reviewed'
    )
    review_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha de revisión'
    )
    
    class Meta:
        verbose_name = 'Solicitud Simplificada de Adopción'
        verbose_name_plural = 'Solicitudes de Adopción'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.full_name} - {self.pet.name} ({self.status})"