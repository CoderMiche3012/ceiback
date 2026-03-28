from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from beneficiarios.models import Direccion, Expediente
from .serializers import DireccionSerializer, ExpedienteSerializer

class DireccionViewSet(viewsets.ModelViewSet):
    queryset = Direccion.objects.all()
    serializer_class = DireccionSerializer
    permission_classes = [IsAuthenticated] 

class ExpedienteViewSet(viewsets.ModelViewSet):
    queryset = Expediente.objects.all()
    serializer_class = ExpedienteSerializer
    permission_classes = [IsAuthenticated]