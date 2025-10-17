from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import AdminUser, AdminActivityLog


class AdminUserSerializer(serializers.ModelSerializer):
    """
    Serializer para el usuario administrador
    """
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = AdminUser
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 
            'full_name', 'phone', 'role', 'profile_picture', 
            'is_active', 'last_activity', 'date_joined'
        ]
        read_only_fields = ['id', 'date_joined', 'last_activity']


class LoginSerializer(serializers.Serializer):
    """
    Serializer para el login de administradores
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            
            if user:
                if not user.is_active:
                    raise serializers.ValidationError('La cuenta está desactivada.')
                data['user'] = user
            else:
                raise serializers.ValidationError('Credenciales incorrectas.')
        else:
            raise serializers.ValidationError('Debe incluir username y password.')
        
        return data


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer para cambiar contraseña
    """
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)
    
    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        return data


class AdminActivityLogSerializer(serializers.ModelSerializer):
    """
    Serializer para logs de actividad
    """
    user_username = serializers.CharField(source='user.username', read_only=True)
    action_display = serializers.CharField(source='get_action_display', read_only=True)
    
    class Meta:
        model = AdminActivityLog
        fields = ['id', 'user', 'user_username', 'action', 'action_display', 
                  'description', 'ip_address', 'created_at']
        read_only_fields = ['id', 'created_at']