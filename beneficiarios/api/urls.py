from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DireccionViewSet, ExpedienteViewSet

router = DefaultRouter()
router.register(r'direcciones', DireccionViewSet, basename='direcciones')
router.register(r'expedientes', ExpedienteViewSet, basename='expedientes')

urlpatterns = [
    path('', include(router.urls)),
]