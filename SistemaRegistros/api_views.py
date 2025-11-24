"""
ViewSets para Django REST Framework - ES03
"""

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from .models import Visita
from .serializers import (
    VisitaSerializer,
    VisitaListSerializer,
    VisitaCreateSerializer,
    VisitaUpdateSerializer,
    UserSerializer
)


class VisitaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD sobre Visita
    
    Endpoints generados automáticamente:
    - GET /api/visitas/ - Listar todas las visitas
    - POST /api/visitas/ - Crear una visita
    - GET /api/visitas/{id}/ - Obtener una visita específica
    - PUT /api/visitas/{id}/ - Actualizar una visita completa
    - PATCH /api/visitas/{id}/ - Actualizar parcialmente una visita
    - DELETE /api/visitas/{id}/ - Eliminar una visita
    """
    
    queryset = Visita.objects.all().order_by('-fecha_entrada')
    serializer_class = VisitaSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        """
        Retorna el serializer apropiado según la acción
        """
        if self.action == 'list':
            return VisitaListSerializer
        elif self.action == 'create':
            return VisitaCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return VisitaUpdateSerializer
        return VisitaSerializer
    
    def list(self, request, *args, **kwargs):
        """
        Lista todas las visitas con paginación
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """
        Crea una nueva visita
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    
    def retrieve(self, request, *args, **kwargs):
        """
        Obtiene una visita específica
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        """
        Actualiza una visita completa
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)
    
    def partial_update(self, request, *args, **kwargs):
        """
        Actualiza parcialmente una visita
        """
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """
        Elimina una visita
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Visita eliminada exitosamente"},
            status=status.HTTP_204_NO_CONTENT
        )
    
    @action(detail=False, methods=['get'])
    def activas(self, request):
        """
        Endpoint personalizado: /api/visitas/activas/
        Retorna solo las visitas activas (sin hora de salida)
        """
        visitas_activas = self.queryset.filter(hora_salida__isnull=True)
        serializer = self.get_serializer(visitas_activas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def completadas(self, request):
        """
        Endpoint personalizado: /api/visitas/completadas/
        Retorna solo las visitas completadas (con hora de salida)
        """
        visitas_completadas = self.queryset.filter(hora_salida__isnull=False)
        serializer = self.get_serializer(visitas_completadas, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def marcar_salida(self, request, pk=None):
        """
        Endpoint personalizado: /api/visitas/{id}/marcar_salida/
        Marca la hora de salida de una visita
        """
        from django.utils import timezone
        
        visita = self.get_object()
        if visita.hora_salida:
            return Response(
                {"error": "Esta visita ya tiene hora de salida registrada"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        visita.hora_salida = timezone.now().time()
        visita.save()
        
        serializer = self.get_serializer(visita)
        return Response(serializer.data)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet de solo lectura para usuarios
    Solo para obtener información del usuario autenticado
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Endpoint: /api/users/me/
        Retorna la información del usuario actual
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class PublicVisitaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet público de solo lectura para visitas
    No requiere autenticación - útil para displays públicos
    """
    queryset = Visita.objects.all().order_by('-fecha_entrada')[:10]
    serializer_class = VisitaListSerializer
    permission_classes = [AllowAny]
    pagination_class = None
