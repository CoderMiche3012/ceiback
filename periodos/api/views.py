from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from periodos.models import Periodo
from .serializers import PeriodoSerializer

class PeriodoViewSet(viewsets.ModelViewSet):
    queryset = Periodo.objects.all()
    serializer_class = PeriodoSerializer
    # Por ahora exigimos que estén logueados para crear o editar periodos
    permission_classes = [IsAuthenticated]