from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegistroUsuarioView, UsuarioViewSet, RolViewSet, PermisoViewSet

# El DefaultRouter de DRF crea automáticamente las URLs para los ViewSets (listar, crear, borrar, etc.)
router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuarios')
router.register(r'roles', RolViewSet, basename='roles')
router.register(r'permisos', PermisoViewSet, basename='permisos')

urlpatterns = [
    # Esta es tu ruta específica para que la gente se registre: /api/cuentas/registro/
    path('registro/', RegistroUsuarioView.as_view(), name='registro_usuario'),
    
    # Esto incluye todas las rutas automáticas del router bajo: /api/cuentas/...
    path('', include(router.urls)),
]