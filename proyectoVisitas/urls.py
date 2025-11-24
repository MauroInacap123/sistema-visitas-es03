"""
URLs principales del proyecto - ES03
Incluye rutas para API REST con JWT
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from SistemaRegistros.api_views import VisitaViewSet, UserViewSet, PublicVisitaViewSet

# Configurar router de DRF
router = DefaultRouter()
router.register(r'visitas', VisitaViewSet, basename='visita')
router.register(r'users', UserViewSet, basename='user')
router.register(r'public/visitas', PublicVisitaViewSet, basename='public-visita')

urlpatterns = [
    # Admin de Django
    path('admin/', admin.site.urls),
    
    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # API REST
    path('api/', include(router.urls)),
    
    # API Auth (opcional - para navegador)
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    # Vistas tradicionales de Django (templates)
    path('', include('SistemaRegistros.urls')),
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
