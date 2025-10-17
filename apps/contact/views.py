from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import ContactMessage
from .serializers import (
    ContactMessageSerializer,
    ContactMessageCreateSerializer,
    ContactMessageResponseSerializer
)
from apps.common.permissions import IsAdminUser


class ContactMessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet para mensajes de contacto
    
    list: GET /api/contact/messages/ - Listar mensajes (admin)
    retrieve: GET /api/contact/messages/{id}/ - Detalle (admin)
    create: POST /api/contact/messages/ - Crear mensaje (público)
    update: PUT/PATCH /api/contact/messages/{id}/ - Actualizar (admin)
    destroy: DELETE /api/contact/messages/{id}/ - Eliminar (admin)
    """
    queryset = ContactMessage.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['subject', 'status']
    search_fields = ['full_name', 'email', 'message']
    ordering_fields = ['created_at', 'status']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ContactMessageCreateSerializer
        elif self.action == 'respond':
            return ContactMessageResponseSerializer
        return ContactMessageSerializer
    
    def get_permissions(self):
        # Solo 'create' es público
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def create(self, request, *args, **kwargs):
        """
        Crear nuevo mensaje de contacto (público)
        POST /api/contact/messages/
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            message = serializer.save()
            
            return Response({
                'message': 'Mensaje enviado exitosamente. Nos pondremos en contacto pronto.',
                'message_id': message.id
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated, IsAdminUser])
    def respond(self, request, pk=None):
        """
        Responder a un mensaje de contacto
        PATCH /api/contact/messages/{id}/respond/
        Body: {
            "admin_response": "Gracias por tu mensaje...",
            "status": "resolved"
        }
        """
        message = self.get_object()
        serializer = ContactMessageResponseSerializer(
            message,
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save()
            
            return Response({
                'message': 'Respuesta enviada exitosamente',
                'data': ContactMessageSerializer(message).data
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsAdminUser])
    def pending(self, request):
        """
        Obtener mensajes sin responder
        GET /api/contact/messages/pending/
        """
        messages = self.get_queryset().filter(status='new')
        serializer = ContactMessageSerializer(messages, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsAdminUser])
    def statistics(self, request):
        """
        Estadísticas de mensajes
        GET /api/contact/messages/statistics/
        """
        total = self.get_queryset().count()
        new = self.get_queryset().filter(status='new').count()
        in_progress = self.get_queryset().filter(status='in_progress').count()
        resolved = self.get_queryset().filter(status='resolved').count()
        
        return Response({
            'total': total,
            'new': new,
            'in_progress': in_progress,
            'resolved': resolved
        })
    
    def perform_destroy(self, instance):
        # Soft delete
        instance.is_active = False
        instance.save()