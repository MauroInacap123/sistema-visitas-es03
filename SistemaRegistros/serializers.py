"""
Serializers para Django REST Framework - ES03
"""

from rest_framework import serializers
from .models import Visita
from django.contrib.auth.models import User


class VisitaSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Visita
    Convierte objetos Visita a JSON y viceversa
    """
    
    class Meta:
        model = Visita
        fields = ['id', 'rut', 'nombre', 'motivo', 'fecha_entrada', 'hora_salida']
        read_only_fields = ['id', 'fecha_entrada']
    
    def validate_rut(self, value):
        """
        Validación personalizada del RUT
        """
        if not value:
            raise serializers.ValidationError("El RUT es obligatorio")
        
        # El RUT debe tener el formato correcto (ya validado en el modelo)
        return value


class VisitaListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listados
    """
    class Meta:
        model = Visita
        fields = ['id', 'rut', 'nombre', 'motivo', 'fecha_entrada', 'hora_salida']


class VisitaCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para crear visitas
    """
    class Meta:
        model = Visita
        fields = ['rut', 'nombre', 'motivo']
    
    def create(self, validated_data):
        """
        Crea una nueva visita
        """
        return Visita.objects.create(**validated_data)


class VisitaUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para actualizar visitas
    """
    class Meta:
        model = Visita
        fields = ['rut', 'nombre', 'motivo', 'hora_salida']
    
    def update(self, instance, validated_data):
        """
        Actualiza una visita existente
        """
        instance.rut = validated_data.get('rut', instance.rut)
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.motivo = validated_data.get('motivo', instance.motivo)
        instance.hora_salida = validated_data.get('hora_salida', instance.hora_salida)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo User (opcional)
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']
