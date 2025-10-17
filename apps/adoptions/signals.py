from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import SimplifiedAdoptionRequest, AdoptionApplication


@receiver(post_save, sender=SimplifiedAdoptionRequest)
def update_pet_status_on_approval(sender, instance, **kwargs):
    """
    Cuando una solicitud se aprueba, actualizar el estado de la mascota
    """
    if instance.status == 'Aprobada':
        pet = instance.pet
        pet.status = 'adopted'
        pet.adoption_date = timezone.now().date()
        pet.save()


@receiver(post_save, sender=AdoptionApplication)
def update_pet_status_on_full_application_approval(sender, instance, **kwargs):
    """
    Para el formulario completo también
    """
    if instance.application_status == 'Aprobada':
        pet = instance.pet
        pet.status = 'adopted'
        pet.adoption_date = timezone.now().date()
        pet.save()