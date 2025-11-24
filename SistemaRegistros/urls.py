"""
URLs de la aplicación SistemaRegistros
Vistas tradicionales de Django (templates)
"""

from django.urls import path
from . import views

urlpatterns = [
    # Vistas tradicionales (templates)
    path('', views.lista_visitas, name='lista_visitas'),
    path('registrar/', views.registrar_visita, name='registrar_visita'),
    path('editar/<int:pk>/', views.editar_visita, name='editar_visita'),
    path('eliminar/<int:pk>/', views.eliminar_visita, name='eliminar_visita'),
]
