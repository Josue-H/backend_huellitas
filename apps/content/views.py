from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import NewsArticle, SuccessStory, FAQ
from .serializers import (
    NewsArticleSerializer,
    SuccessStorySerializer,
    FAQSerializer
)
from apps.common.permissions import IsAdminUser


class NewsArticleViewSet(viewsets.ModelViewSet):
    """
    ViewSet para artículos de noticias
    """
    queryset = NewsArticle.objects.all()
    serializer_class = NewsArticleSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_featured', 'is_active']
    search_fields = ['title', 'summary', 'content']
    ordering_fields = ['published_date', 'title']
    ordering = ['-published_date']
    # lookup_field = 'slug'  # ← COMENTAR O ELIMINAR ESTA LÍNEA
    
    def get_object(self):
        """
        Buscar noticia por ID o slug
        """
        lookup_value = self.kwargs.get('pk')
        queryset = self.get_queryset()
        
        # Intentar buscar por ID si es un número
        if lookup_value.isdigit():
            try:
                return queryset.get(pk=int(lookup_value))
            except NewsArticle.DoesNotExist:
                pass
        
        # Si no es número o no se encontró, buscar por slug
        try:
            return queryset.get(slug=lookup_value)
        except NewsArticle.DoesNotExist:
            from django.http import Http404
            raise Http404("Noticia no encontrada")
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'featured']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        queryset = NewsArticle.objects.all()
        
        # Si no es admin, solo mostrar activos
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_active=True)
        
        return queryset
    
    def perform_create(self, serializer):
        # Asignar el usuario actual como autor
        serializer.save(author=self.request.user)
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def featured(self, request):
        """
        Obtener artículos destacados
        GET /api/content/news/featured/
        """
        articles = self.get_queryset().filter(is_featured=True, is_active=True)[:3]
        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)
    
    def perform_destroy(self, instance):
        # Soft delete
        instance.is_active = False
        instance.save()


class SuccessStoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet para historias de éxito
    
    list: GET /api/content/success-stories/ - Listar (público)
    retrieve: GET /api/content/success-stories/{id}/ - Detalle (público)
    create: POST /api/content/success-stories/ - Crear (admin)
    update: PUT/PATCH /api/content/success-stories/{id}/ - Actualizar (admin)
    destroy: DELETE /api/content/success-stories/{id}/ - Eliminar (admin)
    """
    queryset = SuccessStory.objects.all()
    serializer_class = SuccessStorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_featured', 'is_active']
    search_fields = ['title', 'pet_name', 'adopter_name', 'story']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'featured']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        queryset = SuccessStory.objects.all()
        
        # Si no es admin, solo mostrar activos
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_active=True)
        
        return queryset
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def featured(self, request):
        """
        Obtener historias destacadas
        GET /api/content/success-stories/featured/
        """
        stories = self.get_queryset().filter(is_featured=True, is_active=True)[:4]
        serializer = self.get_serializer(stories, many=True)
        return Response(serializer.data)
    
    def perform_destroy(self, instance):
        # Soft delete
        instance.is_active = False
        instance.save()


class FAQViewSet(viewsets.ModelViewSet):
    """
    ViewSet para preguntas frecuentes
    
    list: GET /api/content/faqs/ - Listar (público)
    retrieve: GET /api/content/faqs/{id}/ - Detalle (público)
    create: POST /api/content/faqs/ - Crear (admin)
    update: PUT/PATCH /api/content/faqs/{id}/ - Actualizar (admin)
    destroy: DELETE /api/content/faqs/{id}/ - Eliminar (admin)
    """
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['category', 'is_active']
    ordering_fields = ['order', 'category']
    ordering = ['category', 'order']
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'by_category']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        queryset = FAQ.objects.all()
        
        # Si no es admin, solo mostrar activos
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_active=True)
        
        return queryset
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def by_category(self, request):
        """
        Obtener FAQs agrupados por categoría
        GET /api/content/faqs/by_category/
        """
        faqs = self.get_queryset().filter(is_active=True)
        
        # Agrupar por categoría
        grouped = {}
        for faq in faqs:
            category = faq.get_category_display()
            if category not in grouped:
                grouped[category] = []
            grouped[category].append(FAQSerializer(faq).data)
        
        return Response(grouped)
    
    def perform_destroy(self, instance):
        # Soft delete
        instance.is_active = False
        instance.save()