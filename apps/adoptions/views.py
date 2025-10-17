from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.http import FileResponse, Http404
from django.conf import settings
import os

from .models import AdoptionApplication, PersonalReference, SimplifiedAdoptionRequest
from .serializers import (
    AdoptionApplicationListSerializer,
    AdoptionApplicationDetailSerializer,
    AdoptionApplicationCreateSerializer,
    AdoptionApplicationUpdateStatusSerializer,
    PersonalReferenceSerializer,
    SimplifiedAdoptionRequestSerializer
)
from apps.common.permissions import IsAdminUser


class AdoptionApplicationViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar solicitudes de adopción (formulario completo)
    
    list: GET /api/adoptions/applications/ - Listar solicitudes (admin)
    retrieve: GET /api/adoptions/applications/{id}/ - Detalle de solicitud (admin)
    create: POST /api/adoptions/applications/ - Crear solicitud (público)
    update: PUT /api/adoptions/applications/{id}/ - Actualizar solicitud (admin)
    partial_update: PATCH /api/adoptions/applications/{id}/ - Actualizar parcial (admin)
    """
    queryset = AdoptionApplication.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['application_status', 'pet', 'dwelling_type', 'adoption_purpose']
    search_fields = ['full_name', 'email', 'cell_phone', 'pet__name']
    ordering_fields = ['created_at', 'full_name']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return AdoptionApplicationCreateSerializer
        elif self.action == 'list':
            return AdoptionApplicationListSerializer
        elif self.action == 'update_status':
            return AdoptionApplicationUpdateStatusSerializer
        return AdoptionApplicationDetailSerializer
    
    def get_permissions(self):
        # Solo 'create' es público, el resto requiere autenticación
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        queryset = AdoptionApplication.objects.select_related('pet', 'reviewed_by').prefetch_related('references')
        
        # Filtrar por estado si se proporciona
        status_param = self.request.query_params.get('status', None)
        if status_param:
            queryset = queryset.filter(application_status=status_param)
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        """
        Crear nueva solicitud de adopción (formulario público completo)
        POST /api/adoptions/applications/
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            application = serializer.save()
            
            return Response({
                'message': 'Solicitud de adopción enviada exitosamente',
                'application_id': application.id,
                'data': AdoptionApplicationDetailSerializer(application).data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated, IsAdminUser])
    def update_status(self, request, pk=None):
        """
        Actualizar el estado de una solicitud
        PATCH /api/adoptions/applications/{id}/update_status/
        Body: {
            "application_status": "Aprobada",
            "admin_notes": "Cumple con todos los requisitos"
        }
        """
        application = self.get_object()
        serializer = AdoptionApplicationUpdateStatusSerializer(
            application, 
            data=request.data, 
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save()
            
            # Si se aprueba, actualizar el estado de la mascota
            if serializer.validated_data.get('application_status') == 'Aprobada':
                pet = application.pet
                pet.status = 'in_process'
                pet.save()
            
            return Response({
                'message': 'Estado actualizado exitosamente',
                'data': AdoptionApplicationDetailSerializer(application).data
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsAdminUser])
    def pending(self, request):
        """
        Obtener solicitudes pendientes
        GET /api/adoptions/applications/pending/
        """
        applications = self.get_queryset().filter(application_status='Recibida')
        serializer = AdoptionApplicationListSerializer(applications, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsAdminUser])
    def statistics(self, request):
        """
        Estadísticas de solicitudes
        GET /api/adoptions/applications/statistics/
        """
        total = self.get_queryset().count()
        received = self.get_queryset().filter(application_status='Recibida').count()
        in_review = self.get_queryset().filter(application_status='En Revisión').count()
        approved = self.get_queryset().filter(application_status='Aprobada').count()
        rejected = self.get_queryset().filter(application_status='Rechazada').count()
        
        return Response({
            'total': total,
            'received': received,
            'in_review': in_review,
            'approved': approved,
            'rejected': rejected
        })
    
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated, IsAdminUser])
    def references(self, request, pk=None):
        """
        Obtener referencias de una solicitud
        GET /api/adoptions/applications/{id}/references/
        """
        application = self.get_object()
        references = application.references.all()
        serializer = PersonalReferenceSerializer(references, many=True)
        return Response(serializer.data)
    
    def perform_destroy(self, instance):
        # Soft delete
        instance.is_active = False
        instance.save()


class SimplifiedAdoptionRequestViewSet(viewsets.ModelViewSet):
    """
    ViewSet para solicitudes simplificadas (formulario PDF)
    
    create: POST /api/adoptions/simplified/ - Enviar solicitud (público)
    list: GET /api/adoptions/simplified/ - Listar (admin)
    retrieve: GET /api/adoptions/simplified/{id}/ - Ver detalle (admin)
    """
    queryset = SimplifiedAdoptionRequest.objects.all()
    serializer_class = SimplifiedAdoptionRequestSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'pet']
    search_fields = ['full_name', 'phone', 'pet__name']
    ordering = ['-created_at']
    
    def get_permissions(self):
        # Solo 'create' es público
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def create(self, request, *args, **kwargs):
        """
        Enviar solicitud simplificada
        POST /api/adoptions/simplified/
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            application = serializer.save()
            
            return Response({
                'message': 'Solicitud enviada exitosamente. Nos pondremos en contacto pronto.',
                'application_id': application.id
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def download_adoption_form(request):
    """
    Descargar el formulario de adopción en PDF
    GET /api/adoptions/download-form/
    """
    # Ruta del archivo PDF
    file_path = os.path.join(settings.MEDIA_ROOT, 'forms', 'formulario_adopcion.pdf')
    
    if os.path.exists(file_path):
        return FileResponse(
            open(file_path, 'rb'),
            as_attachment=True,
            filename='Formulario_Adopcion_Huellitas.pdf',
            content_type='application/pdf'
        )
    else:
        raise Http404("El formulario no está disponible en este momento.")