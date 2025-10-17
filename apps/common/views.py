from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

from apps.pets.models import Pet
from apps.adoptions.models import AdoptionApplication
from apps.contact.models import ContactMessage
from apps.content.models import NewsArticle, SuccessStory
from apps.common.permissions import IsAdminUser


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def dashboard_statistics(request):
    """
    Estadísticas generales para el dashboard de administración
    GET /api/dashboard/statistics/
    """
    
    # Estadísticas de Mascotas
    total_pets = Pet.objects.filter(is_active=True).count()
    available_pets = Pet.objects.filter(status='available', is_active=True).count()
    adopted_pets = Pet.objects.filter(status='adopted', is_active=True).count()
    in_process_pets = Pet.objects.filter(status='in_process', is_active=True).count()
    
    # Estadísticas por especie
    pets_by_species = Pet.objects.filter(is_active=True).values('species').annotate(
        count=Count('id')
    )
    
    # Estadísticas de Adopciones
    total_applications = AdoptionApplication.objects.filter(is_active=True).count()
    pending_applications = AdoptionApplication.objects.filter(
        application_status='Recibida', 
        is_active=True
    ).count()
    approved_applications = AdoptionApplication.objects.filter(
        application_status='Aprobada', 
        is_active=True
    ).count()
    rejected_applications = AdoptionApplication.objects.filter(
        application_status='Rechazada', 
        is_active=True
    ).count()
    
    # Aplicaciones del último mes
    last_month = timezone.now() - timedelta(days=30)
    applications_last_month = AdoptionApplication.objects.filter(
        created_at__gte=last_month,
        is_active=True
    ).count()
    
    # Estadísticas de Mensajes de Contacto
    total_messages = ContactMessage.objects.filter(is_active=True).count()
    pending_messages = ContactMessage.objects.filter(
        status='new',
        is_active=True
    ).count()
    resolved_messages = ContactMessage.objects.filter(
        status='resolved',
        is_active=True
    ).count()
    
    # Estadísticas de Contenido
    total_news = NewsArticle.objects.filter(is_active=True).count()
    total_success_stories = SuccessStory.objects.filter(is_active=True).count()
    
    # Actividad reciente (últimas 5 solicitudes)
    recent_applications = AdoptionApplication.objects.filter(
        is_active=True
    ).select_related('pet').order_by('-created_at')[:5]
    
    recent_applications_data = [{
        'id': app.id,
        'full_name': app.full_name,
        'pet_name': app.pet.name,
        'status': app.application_status,
        'created_at': app.created_at
    } for app in recent_applications]
    
    # Mascotas agregadas recientemente (últimas 5)
    recent_pets = Pet.objects.filter(
        is_active=True
    ).order_by('-created_at')[:5]
    
    recent_pets_data = [{
        'id': pet.id,
        'name': pet.name,
        'species': pet.get_species_display(),
        'status': pet.get_status_display(),
        'created_at': pet.created_at
    } for pet in recent_pets]
    
    return Response({
        'pets': {
            'total': total_pets,
            'available': available_pets,
            'adopted': adopted_pets,
            'in_process': in_process_pets,
            'by_species': list(pets_by_species)
        },
        'adoptions': {
            'total': total_applications,
            'pending': pending_applications,
            'approved': approved_applications,
            'rejected': rejected_applications,
            'last_month': applications_last_month
        },
        'messages': {
            'total': total_messages,
            'pending': pending_messages,
            'resolved': resolved_messages
        },
        'content': {
            'news': total_news,
            'success_stories': total_success_stories
        },
        'recent_activity': {
            'applications': recent_applications_data,
            'pets': recent_pets_data
        }
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def quick_stats(request):
    """
    Estadísticas rápidas para widgets del dashboard
    GET /api/dashboard/quick-stats/
    """
    return Response({
        'pending_applications': AdoptionApplication.objects.filter(
            application_status='Recibida', 
            is_active=True
        ).count(),
        'available_pets': Pet.objects.filter(
            status='available', 
            is_active=True
        ).count(),
        'pending_messages': ContactMessage.objects.filter(
            status='new', 
            is_active=True
        ).count(),
        'total_adoptions': Pet.objects.filter(
            status='adopted', 
            is_active=True
        ).count()
    })