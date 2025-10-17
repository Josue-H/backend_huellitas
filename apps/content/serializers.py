from rest_framework import serializers
from .models import NewsArticle, SuccessStory, FAQ


class NewsArticleSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.full_name', read_only=True)
    
    class Meta:
        model = NewsArticle
        fields = '__all__'
        read_only_fields = ['id', 'published_date', 'created_at', 'updated_at']


class SuccessStorySerializer(serializers.ModelSerializer):
    """
    Serializer para historias de éxito / testimonios
    """
    # Usar after_image como la imagen principal para el frontend
    imagen = serializers.SerializerMethodField()
    
    class Meta:
        model = SuccessStory
        fields = [
            'id', 'title', 'pet_name', 'adopter_name', 'story',
            'before_image', 'after_image', 'imagen', 'is_featured',
            'created_at', 'is_active'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_imagen(self, obj):
        """Retornar la URL de la imagen principal (after_image)"""
        request = self.context.get('request')
        if obj.after_image:
            if request:
                return request.build_absolute_uri(obj.after_image.url)
            return obj.after_image.url
        return None


class FAQSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = FAQ
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']