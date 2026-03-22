from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from cuentas.models import Rol, Permiso
from .serializers import UsuarioSerializer, RolSerializer, PermisoSerializer
#bibliotecas para peticion de tokens en login 
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
Usuario = get_user_model()
from .permissions import EsAdminODueno

# 1. Vista específica para el Registro de Usuarios
class RegistroUsuarioView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    # Por ahora dejamos que cualquiera se registre. 
    # En el futuro podríamos limitarlo a que solo un 'Administrador' pueda crear cuentas.
    
    # ---> CAMBIO 1: Dejamos la puerta abierta para el registro
    permission_classes = [AllowAny] 

# 2. ViewSets para el CRUD general (Administración)
# Un ModelViewSet genera automáticamente las rutas GET, POST, PUT, PATCH y DELETE.
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    
    # ---> CAMBIO 2: Aquí ponemos a tu cadenero personalizado
    # Protege las rutas de edición para que nadie modifique a otros (salvo los jefes)
    permission_classes = [IsAuthenticated, EsAdminODueno] 

class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer

class PermisoViewSet(viewsets.ModelViewSet):
    queryset = Permiso.objects.all()
    serializer_class = PermisoSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    # Le decimos que use tu serializador con los datos extra
    serializer_class = CustomTokenObtainPairSerializer