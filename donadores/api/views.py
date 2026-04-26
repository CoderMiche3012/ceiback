from rest_framework import viewsets
from donadores.models import Donador, DonativoDonador
from .serializers import DonadorSerializer, DonativoDonadorSerializer

class DonadorViewSet(viewsets.ModelViewSet):
    queryset = Donador.objects.all()
    serializer_class = DonadorSerializer

class DonativoDonadorViewSet(viewsets.ModelViewSet):
    queryset = DonativoDonador.objects.all()
    serializer_class = DonativoDonadorSerializer