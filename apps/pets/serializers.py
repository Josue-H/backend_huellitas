from rest_framework import serializers
from .models import Pet, PetImage


class PetImageSerializer(serializers.ModelSerializer):
    """
    Serializer para imágenes de mascotas
    """
    class Meta:
        model = PetImage
        fields = ['id', 'image', 'caption', 'order', 'created_at']
        read_only_fields = ['id', 'created_at']


class PetListSerializer(serializers.ModelSerializer):
    """
    Serializer resumido para listado de mascotas
    """
    species_display = serializers.CharField(source='get_species_display', read_only=True)
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    size_display = serializers.CharField(source='get_size_display', read_only=True)
    age_display = serializers.ReadOnlyField()
    
    class Meta:
        model = Pet
        fields = [
            'id', 'name', 'species', 'species_display', 'breed', 
            'gender', 'gender_display', 'age_years', 'age_months', 'age_display',
            'size', 'size_display', 'status', 'status_display', 
            'main_image', 'description',
            'friendly_with_kids', 'adapts_to_indoor_living', 'energy_level',
            'is_active', 'created_at'
        ]


class PetDetailSerializer(serializers.ModelSerializer):
    """
    Serializer completo para detalle de mascota
    """
    species_display = serializers.CharField(source='get_species_display', read_only=True)
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    size_display = serializers.CharField(source='get_size_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    age_display = serializers.ReadOnlyField()
    is_available = serializers.ReadOnlyField()
    images = PetImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Pet
        fields = [
            'id', 'name', 'species', 'species_display', 'breed', 
            'gender', 'gender_display', 'age_years', 'age_months', 
            'age_display', 'size', 'size_display', 'weight', 'color',
            'status', 'status_display', 'is_sterilized', 'is_vaccinated', 
            'is_dewormed', 'description', 'characteristics', 'special_needs',
            'arrival_date', 'adoption_date', 'main_image', 'images',
            'friendly_with_kids', 'adapts_to_indoor_living', 'easy_to_train', 'energy_level',
            'is_active', 'is_available', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'arrival_date', 'created_at', 'updated_at']


class PetCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para crear/actualizar mascotas
    """
    class Meta:
        model = Pet
        fields = [
            'name', 'species', 'breed', 'gender', 'age_years', 'age_months',
            'size', 'weight', 'color', 'status', 'is_sterilized', 
            'is_vaccinated', 'is_dewormed', 'description', 'characteristics',
            'special_needs', 'adoption_date', 'main_image', 'is_active',
            'friendly_with_kids', 'adapts_to_indoor_living', 'easy_to_train', 'energy_level'
        ]
    
    def validate(self, data):
        # Validar que si el status es 'adopted', tenga fecha de adopción
        if data.get('status') == 'adopted' and not data.get('adoption_date'):
            raise serializers.ValidationError({
                'adoption_date': 'La fecha de adopción es requerida para mascotas adoptadas.'
            })
        return data