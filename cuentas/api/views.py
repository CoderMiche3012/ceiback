from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from cuentas.models import Rol, Permiso
from .serializers import UsuarioSerializer, RolSerializer, PermisoSerializer

Usuario = get_user_model()

# 1. Vista específica para el Registro de Usuarios
class RegistroUsuarioView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    # Por ahora dejamos que cualquiera se registre. 
    # En el futuro podríamos limitarlo a que solo un 'Administrador' pueda crear cuentas.
    permission_classes = [AllowAny] 

# 2. ViewSets para el CRUD general (Administración)
# Un ModelViewSet genera automáticamente las rutas GET, POST, PUT, PATCH y DELETE.
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated] # <- Lo descomentaremos cuando configuremos los tokens

class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer

class PermisoViewSet(viewsets.ModelViewSet):
    queryset = Permiso.objects.all()
    serializer_class = PermisoSerializer