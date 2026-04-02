from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DireccionViewSet, ExpedienteViewSet, PostulanteViewSet, VisitaPostulanteViewSet, BeneficiarioViewSet

router = DefaultRouter()
router.register(r'direcciones', DireccionViewSet, basename='direcciones')
router.register(r'expedientes', ExpedienteViewSet, basename='expedientes')
router.register(r'postulantes', PostulanteViewSet, basename='postulantes') 
router.register(r'visitas', VisitaPostulanteViewSet, basename='visitas')
router.register(r'beneficiarios', BeneficiarioViewSet, basename='beneficiarios_finales')

urlpatterns = [
    path('', include(router.urls)),
]
