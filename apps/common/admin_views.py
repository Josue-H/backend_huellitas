from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from apps.pets.models import Pet
from apps.adoptions.models import AdoptionApplication, SimplifiedAdoptionRequest
from apps.contact.models import ContactMessage


@staff_member_required
def admin_dashboard(request):
    """
    Dashboard personalizado para el admin de Django
    """
    # Estadísticas de mascotas
    total_mascotas = Pet.objects.filter(is_active=True).count()
    disponibles = Pet.objects.filter(status='available', is_active=True).count()
    en_proceso = Pet.objects.filter(status='in_process', is_active=True).count()
    adoptados = Pet.objects.filter(status='adopted', is_active=True).count()
    
    # Estadísticas de solicitudes
    solicitudes_pendientes = SimplifiedAdoptionRequest.objects.filter(
        status='Recibida', 
        is_active=True
    ).count()
    solicitudes_revision = SimplifiedAdoptionRequest.objects.filter(
        status='En Revisión', 
        is_active=True
    ).count()
    solicitudes_aprobadas = SimplifiedAdoptionRequest.objects.filter(
        status='Aprobada', 
        is_active=True
    ).count()
    
    # Mensajes de contacto activos
    mensajes_nuevos = ContactMessage.objects.filter(
        status='new', 
        is_active=True
    ).count()
    mensajes_proceso = ContactMessage.objects.filter(
        status='in_progress', 
        is_active=True
    ).count()
    
    # Actividad reciente
    ultimas_solicitudes = SimplifiedAdoptionRequest.objects.filter(
        is_active=True
    ).select_related('pet').order_by('-created_at')[:5]
    
    ultimas_mascotas = Pet.objects.filter(
        is_active=True
    ).order_by('-created_at')[:5]
    
    context = {
        'title': 'Dashboard Huellitas',
        'total_mascotas': total_mascotas,
        'disponibles': disponibles,
        'en_proceso': en_proceso,
        'adoptados': adoptados,
        'solicitudes_pendientes': solicitudes_pendientes,
        'solicitudes_revision': solicitudes_revision,
        'solicitudes_aprobadas': solicitudes_aprobadas,
        'mensajes_nuevos': mensajes_nuevos,
        'mensajes_proceso': mensajes_proceso,
        'ultimas_solicitudes': ultimas_solicitudes,
        'ultimas_mascotas': ultimas_mascotas,
    }
    
    return render(request, 'admin/dashboard.html', context)