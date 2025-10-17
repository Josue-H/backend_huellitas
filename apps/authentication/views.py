from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from .models import AdminUser, AdminActivityLog
from .serializers import (
    AdminUserSerializer, 
    LoginSerializer, 
    ChangePasswordSerializer,
    AdminActivityLogSerializer
)


def get_client_ip(request):
    """Obtener IP del cliente"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@api_view(['POST'])
@permission_classes([AllowAny])
def admin_login(request):
    """
    Login para administradores
    POST /api/auth/login/
    """
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        
        # Crear o obtener token
        token, created = Token.objects.get_or_create(user=user)
        
        # Actualizar sesión activa
        user.is_active_session = True
        user.save()
        
        # Registrar actividad
        AdminActivityLog.objects.create(
            user=user,
            action='login',
            description=f'Inicio de sesión exitoso',
            ip_address=get_client_ip(request)
        )
        
        return Response({
            'token': token.key,
            'user': AdminUserSerializer(user).data,
            'message': 'Login exitoso'
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_logout(request):
    """
    Logout para administradores
    POST /api/auth/logout/
    """
    try:
        # Eliminar token
        request.user.auth_token.delete()
        
        # Actualizar sesión
        request.user.is_active_session = False
        request.user.save()
        
        # Registrar actividad
        AdminActivityLog.objects.create(
            user=request.user,
            action='logout',
            description='Cierre de sesión',
            ip_address=get_client_ip(request)
        )
        
        return Response({
            'message': 'Logout exitoso'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_admin_user(request):
    """
    Obtener información del usuario actual
    GET /api/auth/me/
    """
    serializer = AdminUserSerializer(request.user)
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_admin_profile(request):
    """
    Actualizar perfil del administrador
    PUT/PATCH /api/auth/profile/
    """
    serializer = AdminUserSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """
    Cambiar contraseña
    POST /api/auth/change-password/
    """
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        user = request.user
        
        # Verificar contraseña actual
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({
                'old_password': 'Contraseña incorrecta'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Cambiar contraseña
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        # Registrar actividad
        AdminActivityLog.objects.create(
            user=user,
            action='update_content',
            description='Cambio de contraseña',
            ip_address=get_client_ip(request)
        )
        
        return Response({
            'message': 'Contraseña actualizada exitosamente'
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminActivityLogListView(generics.ListAPIView):
    """
    Listar logs de actividad
    GET /api/auth/activity-logs/
    """
    serializer_class = AdminActivityLogSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Solo super_admin puede ver todos los logs
        if self.request.user.role == 'super_admin':
            return AdminActivityLog.objects.all()
        # Otros solo ven sus propios logs
        return AdminActivityLog.objects.filter(user=self.request.user)