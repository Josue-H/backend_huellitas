from django.contrib import admin
from django.urls import path, include
from django.conf import settings               
from django.conf.urls.static import static
from apps.common.api_root import api_root

urlpatterns = [
    # Página de inicio de la API
    path('', api_root, name='api-root'),
    
    # Django Admin (opcional, para desarrollo)
    path('admin/', admin.site.urls),
    
    # API Routes - Panel de Administración
    path('api/auth/', include('apps.authentication.urls')),
    path('api/', include('apps.pets.urls')),
    path('api/adoptions/', include('apps.adoptions.urls')),
    path('api/contact/', include('apps.contact.urls')),
    path('api/content/', include('apps.content.urls')),
    path('api/', include('apps.common.urls')),
]

# Servir archivos de media y static en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)