from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from estudios.models import Estudio_Socioeconomico, Familia
from .serializers import EstudioSocioeconomicoSerializer, FamiliaSerializer

class EstudioSocioeconomicoViewSet(viewsets.ModelViewSet):
    queryset = Estudio_Socioeconomico.objects.all()
    serializer_class = EstudioSocioeconomicoSerializer
    permission_classes = [IsAuthenticated] # O AllowAny para pruebas

class FamiliaViewSet(viewsets.ModelViewSet):
    queryset = Familia.objects.all()
    serializer_class = FamiliaSerializer