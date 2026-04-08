from django.urls import path, include
from rest_framework.routers import DefaultRouter
# 1. Asegúrate de importar el ViewSet de Familia aquí
from .views import EstudioSocioeconomicoViewSet, FamiliaViewSet 

router = DefaultRouter()
router.register(r'estudios', EstudioSocioeconomicoViewSet, basename='estudios-socioeconomicos')

# 2. Registramos la nueva ruta para los familiares
router.register(r'familia', FamiliaViewSet, basename='familia')

urlpatterns = [
    path('', include(router.urls)),
]