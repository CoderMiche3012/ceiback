from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from periodos.models import Periodo
from .serializers import PeriodoSerializer

class PeriodoViewSet(viewsets.ModelViewSet):
    queryset = Periodo.objects.all()
    serializer_class = PeriodoSerializer
    permission_classes = [IsAuthenticated]