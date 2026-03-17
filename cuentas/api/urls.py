from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView # <-- IMPORTANTE
from .views import RegistroUsuarioView, UsuarioViewSet, RolViewSet, PermisoViewSet

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuarios')
router.register(r'roles', RolViewSet, basename='roles')
router.register(r'permisos', PermisoViewSet, basename='permisos')

urlpatterns = [
    # --- RUTAS DE AUTENTICACIÓN ---
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # --- RUTAS DE USUARIOS ---
    path('registro/', RegistroUsuarioView.as_view(), name='registro_usuario'),
    path('', include(router.urls)),
]