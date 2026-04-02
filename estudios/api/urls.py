from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EstudioSocioeconomicoViewSet

router = DefaultRouter()
router.register(r'estudios', EstudioSocioeconomicoViewSet, basename='estudios-socioeconomicos')

urlpatterns = [
    path('', include(router.urls)),
]