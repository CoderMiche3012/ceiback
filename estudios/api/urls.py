from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EstudioSocioeconomicoViewSet, FamiliaViewSet, AnalisisViewSet

router = DefaultRouter()
router.register(r'estudios', EstudioSocioeconomicoViewSet, basename='estudios-socioeconomicos')
router.register(r'familia', FamiliaViewSet, basename='familia')
router.register(r'analisis', AnalisisViewSet, basename='analisis')

urlpatterns = [
    path('', include(router.urls)),
]