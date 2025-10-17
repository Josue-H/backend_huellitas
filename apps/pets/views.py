from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Pet, PetImage
from .serializers import (
    PetListSerializer, 
    PetDetailSerializer, 
    PetCreateUpdateSerializer,
    PetImageSerializer
)
from apps.common.permissions import IsAdminUser


class PetViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar mascotas
    
    list: GET /api/pets/ - Listar mascotas (público)
    retrieve: GET /api/pets/{id}/ - Detalle de mascota (público)
    create: POST /api/pets/ - Crear mascota (admin)
    update: PUT /api/pets/{id}/ - Actualizar mascota (admin)
    partial_update: PATCH /api/pets/{id}/ - Actualizar parcial (admin)
    destroy: DELETE /api/pets/{id}/ - Eliminar mascota (admin)
    """
    queryset = Pet.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['species', 'gender', 'size', 'status', 'is_sterilized', 'is_vaccinated']
    search_fields = ['name', 'breed', 'description']
    ordering_fields = ['created_at', 'name', 'age_years']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PetListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return PetCreateUpdateSerializer
        return PetDetailSerializer
    
    def get_permissions(self):
        # Público puede ver (list, retrieve), solo admins pueden modificar
        if self.action in ['list', 'retrieve', 'available']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        queryset = Pet.objects.all()
        
        # Si no es admin, solo mostrar mascotas activas
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_active=True)
        
        return queryset
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def available(self, request):
        """
        Obtener solo mascotas disponibles para adopción
        GET /api/pets/available/
        """
        pets = Pet.objects.filter(status='available', is_active=True)
        serializer = PetListSerializer(pets, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdminUser])
    def upload_images(self, request, pk=None):
        """
        Subir imágenes adicionales a una mascota
        POST /api/pets/{id}/upload_images/
        """
        pet = self.get_object()
        images = request.FILES.getlist('images')
        
        if not images:
            return Response({
                'error': 'No se enviaron imágenes'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        created_images = []
        for image in images:
            pet_image = PetImage.objects.create(
                pet=pet,
                image=image,
                caption=request.data.get('caption', '')
            )
            created_images.append(PetImageSerializer(pet_image).data)
        
        return Response({
            'message': f'{len(created_images)} imágenes subidas exitosamente',
            'images': created_images
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated, IsAdminUser])
    def change_status(self, request, pk=None):
        """
        Cambiar el estado de una mascota
        PATCH /api/pets/{id}/change_status/
        Body: {"status": "adopted", "adoption_date": "2024-01-15"}
        """
        pet = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in dict(Pet.STATUS_CHOICES):
            return Response({
                'error': 'Estado inválido'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        pet.status = new_status
        
        if new_status == 'adopted':
            adoption_date = request.data.get('adoption_date')
            if adoption_date:
                pet.adoption_date = adoption_date
        
        pet.save()
        
        return Response({
            'message': 'Estado actualizado exitosamente',
            'pet': PetDetailSerializer(pet).data
        })
    
    def perform_destroy(self, instance):
        # Soft delete: marcar como inactivo en lugar de eliminar
        instance.is_active = False
        instance.save()


class PetImageViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar imágenes de mascotas
    """
    queryset = PetImage.objects.all()
    serializer_class = PetImageSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def perform_destroy(self, instance):
        # Soft delete
        instance.is_active = False
        instance.save()