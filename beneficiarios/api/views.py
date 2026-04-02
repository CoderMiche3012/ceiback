from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from beneficiarios.models import Direccion, Expediente, Postulante, Visita_Postulante, Beneficiario
from .serializers import DireccionSerializer, ExpedienteSerializer, PostulanteSerializer, VisitaPostulanteSerializer, BeneficiarioSerializer


class DireccionViewSet(viewsets.ModelViewSet):
    queryset = Direccion.objects.all()
    serializer_class = DireccionSerializer
    permission_classes = [IsAuthenticated] 

class ExpedienteViewSet(viewsets.ModelViewSet):
    queryset = Expediente.objects.all()
    serializer_class = ExpedienteSerializer
    permission_classes = [IsAuthenticated]

class PostulanteViewSet(viewsets.ModelViewSet):
    queryset = Postulante.objects.all()
    serializer_class = PostulanteSerializer
    permission_classes = [IsAuthenticated] # O AllowAny si sigues haciendo pruebas sin token

class VisitaPostulanteViewSet(viewsets.ModelViewSet):
    queryset = Visita_Postulante.objects.all()
    serializer_class = VisitaPostulanteSerializer
    permission_classes = [IsAuthenticated]



class BeneficiarioViewSet(viewsets.ModelViewSet):
    queryset = Beneficiario.objects.all()
    serializer_class = BeneficiarioSerializer
    permission_classes = [IsAuthenticated]