from rest_framework import serializers
from .models import AdoptionApplication, PersonalReference
from apps.pets.serializers import PetListSerializer
from .models import AdoptionApplication, PersonalReference, SimplifiedAdoptionRequest


class PersonalReferenceSerializer(serializers.ModelSerializer):
    """
    Serializer para referencias personales
    """
    class Meta:
        model = PersonalReference
        fields = ['id', 'full_name', 'phone', 'relationship']
        read_only_fields = ['id']


class AdoptionApplicationListSerializer(serializers.ModelSerializer):
    """
    Serializer resumido para listado de solicitudes
    """
    pet_name = serializers.CharField(source='pet.name', read_only=True)
    pet_species = serializers.CharField(source='pet.get_species_display', read_only=True)
    status_display = serializers.CharField(source='get_application_status_display', read_only=True)
    
    class Meta:
        model = AdoptionApplication
        fields = [
            'id', 'full_name', 'email', 'cell_phone', 'pet', 'pet_name', 
            'pet_species', 'application_status', 'status_display', 
            'created_at', 'is_active'
        ]
        read_only_fields = ['id', 'created_at']


class AdoptionApplicationDetailSerializer(serializers.ModelSerializer):
    """
    Serializer completo para detalle de solicitud
    """
    pet_detail = PetListSerializer(source='pet', read_only=True)
    references = PersonalReferenceSerializer(many=True, read_only=True)
    reviewed_by_name = serializers.CharField(source='reviewed_by.full_name', read_only=True)
    status_display = serializers.CharField(source='get_application_status_display', read_only=True)
    housing_ownership_display = serializers.CharField(source='get_housing_ownership_display', read_only=True)
    dwelling_type_display = serializers.CharField(source='get_dwelling_type_display', read_only=True)
    adoption_purpose_display = serializers.CharField(source='get_adoption_purpose_display', read_only=True)
    
    class Meta:
        model = AdoptionApplication
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'reviewed_by', 'review_date']


class AdoptionApplicationCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para crear solicitud de adopción (formulario público)
    """
    references = PersonalReferenceSerializer(many=True)
    
    class Meta:
        model = AdoptionApplication
        fields = [
            'pet', 'full_name', 'age', 'civil_status', 'profession', 'address',
            'home_phone', 'cell_phone', 'email', 'housing_ownership', 
            'landlord_permission', 'dwelling_type', 'adoption_reason',
            'pet_location_in_home', 'adults_in_home', 'children_in_home',
            'all_family_agrees', 'can_afford_pet', 'has_had_pets_before',
            'previous_pet_experience', 'has_current_pets', 'current_pets_info',
            'adoption_purpose', 'aware_of_potential_damage', 'damage_plan',
            'willing_to_educate', 'behavior_plan', 'agrees_to_home_visits',
            'home_visit_reasoning', 'understands_no_transfer_policy',
            'vision_in_5_years', 'agrees_to_sterilize', 'dpi_copy',
            'utility_bill_copy', 'references'
        ]
    
    def validate(self, data):
        # Validar que tenga 3 referencias
        references = data.get('references', [])
        if len(references) != 3:
            raise serializers.ValidationError({
                'references': 'Se requieren exactamente 3 referencias personales.'
            })
        
        # Validar landlord_permission si es alquilada
        if data.get('housing_ownership') == 'Alquilada' and data.get('landlord_permission') is None:
            raise serializers.ValidationError({
                'landlord_permission': 'Este campo es requerido para viviendas alquiladas.'
            })
        
        return data
    
    def create(self, validated_data):
        references_data = validated_data.pop('references')
        application = AdoptionApplication.objects.create(**validated_data)
        
        # Crear referencias
        for reference_data in references_data:
            PersonalReference.objects.create(application=application, **reference_data)
        
        return application


class AdoptionApplicationUpdateStatusSerializer(serializers.ModelSerializer):
    """
    Serializer para que los administradores actualicen el estado
    """
    class Meta:
        model = AdoptionApplication
        fields = ['application_status', 'admin_notes']
    
    def update(self, instance, validated_data):
        from django.utils import timezone
        
        instance.application_status = validated_data.get('application_status', instance.application_status)
        instance.admin_notes = validated_data.get('admin_notes', instance.admin_notes)
        
        # Registrar quien revisó y cuándo
        if 'application_status' in validated_data:
            instance.reviewed_by = self.context['request'].user
            instance.review_date = timezone.now()
        
        instance.save()
        return instance


class SimplifiedAdoptionRequestSerializer(serializers.ModelSerializer):
    """
    Serializer para solicitud simplificada (formulario PDF)
    """
    pet_name = serializers.CharField(source='pet.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = SimplifiedAdoptionRequest  # IMPORTANTE: Usar el modelo correcto
        fields = [
            'id', 'pet', 'pet_name', 'full_name', 'pet_name_requested',
            'phone', 'email', 'filled_form_pdf', 'status', 'status_display',
            'created_at'
        ]
        read_only_fields = ['id', 'status', 'created_at']
    
    def validate_filled_form_pdf(self, value):
        # Validar que sea un PDF
        if not value.name.endswith('.pdf'):
            raise serializers.ValidationError('El archivo debe ser un PDF')
        
        # Validar tamaño (máximo 10MB)
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError('El archivo no debe superar los 10MB')
        
        return value