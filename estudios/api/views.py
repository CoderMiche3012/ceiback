from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from estudios.models import EstudioSocioeconomico, Familia, Analisis
from .serializers import EstudioSocioeconomicoSerializer, FamiliaSerializer, AnalisisSerializer

class EstudioSocioeconomicoViewSet(viewsets.ModelViewSet):
    queryset = EstudioSocioeconomico.objects.all()
    serializer_class = EstudioSocioeconomicoSerializer
    permission_classes = [IsAuthenticated]

class FamiliaViewSet(viewsets.ModelViewSet):
    queryset = Familia.objects.all()
    serializer_class = FamiliaSerializer

class AnalisisViewSet(viewsets.ModelViewSet):
    queryset = Analisis.objects.all()
    serializer_class = AnalisisSerializer