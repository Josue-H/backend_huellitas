from rest_framework import serializers
from .models import ContactMessage


class ContactMessageSerializer(serializers.ModelSerializer):
    """
    Serializer para mensajes de contacto
    """
    subject_display = serializers.CharField(source='get_subject_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    responded_by_name = serializers.CharField(source='responded_by.full_name', read_only=True)
    
    class Meta:
        model = ContactMessage
        fields = [
            'id', 'full_name', 'email', 'phone', 'subject', 'subject_display',
            'message', 'status', 'status_display', 'admin_response', 
            'responded_by', 'responded_by_name', 'response_date',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'responded_by', 'response_date']


class ContactMessageCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para crear mensaje de contacto (público)
    """
    class Meta:
        model = ContactMessage
        fields = ['full_name', 'email', 'phone', 'subject', 'message']


class ContactMessageResponseSerializer(serializers.ModelSerializer):
    """
    Serializer para que admins respondan mensajes
    """
    class Meta:
        model = ContactMessage
        fields = ['admin_response', 'status']
    
    def update(self, instance, validated_data):
        from django.utils import timezone
        
        instance.admin_response = validated_data.get('admin_response', instance.admin_response)
        instance.status = validated_data.get('status', instance.status)
        instance.responded_by = self.context['request'].user
        instance.response_date = timezone.now()
        instance.save()
        
        return instance