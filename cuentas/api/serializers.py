import re
from rest_framework import serializers
from django.contrib.auth import get_user_model
from cuentas.models import Rol, Permiso
#biblioteca para peticion de login 
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
Usuario = get_user_model()

class PermisoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permiso
        fields = '__all__'

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'id_usuario', 'nom_usuario', 'nombre', 'apellido_p', 
            'apellido_m', 'correo', 'telefono', 'id_rol', 'estatus', 'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True} # Oculta la contraseña en las respuestas
        }

    # 1. Validación del Teléfono (Exactamente 10 dígitos)
    def validate_telefono(self, value):
        if value and not re.match(r'^\d{10}$', value):
            raise serializers.ValidationError("El teléfono debe contener exactamente 10 números.")
        return value

    # 2. Validación de la Contraseña (Seguridad fuerte)
    def validate_password(self, value):
        # Mínimo 8 caracteres, al menos una letra y un número
        patron = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'
        if not re.match(patron, value):
            raise serializers.ValidationError("La contraseña debe tener al menos 8 caracteres, incluyendo una letra y un número.")
        return value

    # 3. Validación del Nombre de Usuario (Sin espacios, solo letras, números y guiones bajos)
    def validate_nom_usuario(self, value):
        if not re.match(r'^[\w]+$', value):
            raise serializers.ValidationError("El nombre de usuario solo puede contener letras, números y guiones bajos, sin espacios.")
        return value

    # 4. Validación de Nombre y Apellidos (Solo letras y espacios)
    def validate_nombre(self, value):
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', value):
            raise serializers.ValidationError("El nombre solo debe contener letras.")
        return value
    
    def validate_apellido_p(self, value):
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', value):
            raise serializers.ValidationError("El apellido paterno solo debe contener letras.")
        return value
    
    def validate_apellido_m(self, value):
            # El 'if value' permite que el campo se quede en blanco si el usuario no tiene apellido materno
            if value and not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', value):
                raise serializers.ValidationError("El apellido materno solo debe contener letras.")
            return value

    # Creación segura del usuario
    def create(self, validated_data):
        usuario = Usuario.objects.create_user(
            nom_usuario=validated_data['nom_usuario'],
            correo=validated_data['correo'],
            nombre=validated_data['nombre'],
            apellido_p=validated_data['apellido_p'],
            apellido_m=validated_data.get('apellido_m', ''),
            password=validated_data['password'],
            telefono=validated_data.get('telefono', ''),
            id_rol=validated_data.get('id_rol', None)
        )
        return usuario

# optimización de peticion de token para login 
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Primero, dejamos que SimpleJWT valide el usuario y genere el 'access' y 'refresh'
        data = super().validate(attrs)
        #validamos si el usuario esta activo. 
        if not self.user.estatus:
            raise AuthenticationFailed('Esta cuenta ha sido desactivada. Contacta al administrador del sistema.')
        # Luego, inyectamos tu bloque exacto de "user" a la respuesta
        data['user'] = {
            'id': self.user.id_usuario,
            'nombre': self.user.nombre,
            'correo': self.user.correo,
            # Extraemos el nombre del rol si el usuario tiene uno asignado, si no, devolvemos null
            'rol': self.user.id_rol.nombre_rol if self.user.id_rol else None, 
            'estatus': self.user.estatus # Se lo mandamos al front por si quiere usarlo visualmente
        }

        return data
