from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    """
    Vista raíz de la API - Muestra información de endpoints disponibles
    """
    return Response({
        'message': 'Bienvenido a la API de Huellitas 🐾',
        'version': '1.0',
        'endpoints': {
            'public': {
                'pets': '/api/pets/',
                'pets_available': '/api/pets/available/',
                'adoption_apply': '/api/adoptions/applications/',
                'contact': '/api/contact/messages/',
                'news': '/api/content/news/',
                'success_stories': '/api/content/success-stories/',
                'faqs': '/api/content/faqs/'
            },
            'admin': {
                'login': '/api/auth/login/',
                'dashboard': '/api/dashboard/statistics/',
                'admin_panel': '/admin/'
            }
        },
        'documentation': 'Documentación disponible en /api/docs/ (próximamente)'
    })