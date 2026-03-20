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
    password_actual = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Usuario
        # 2. lista actualizada con los pass
        fields = [
            'id_usuario', 'nom_usuario', 'nombre', 'apellido_p', 
            'apellido_m', 'correo', 'telefono', 'id_rol', 'estatus', 
            'password', 'password_actual', 'confirm_password' 
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}
        }
    # 1. Validación del Teléfono (Exactamente 10 dígitos)
    def validate_telefono(self, value):
        if value and not re.match(r'^\d{10}$', value):
            raise serializers.ValidationError("El teléfono debe contener exactamente 10 números.")
        return value

   # 2. Validación de la Contraseña (Seguridad fuerte)
    def validate_password(self, value):
        patron = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[-/#$_@*!?])[A-Za-z\d\-/#$_@*!?]{8,}$'
        
        if not re.match(patron, value):
            raise serializers.ValidationError(
                "La contraseña debe tener al menos 8 caracteres, incluyendo una letra mayúscula, "
                "una minúscula, un número y un carácter especial válido (-/#$_)."
            )
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

    # ACTUALIZACION DE DATOS PERSONALES 
    def validate(self, data):
        # 2. Lógica para cuando se EDITA un perfil existente (self.instance tiene datos)
        if self.instance:
            # Extraemos la contraseña actual que manda React
            password_actual = data.pop('password_actual', None)
            
            # Validamos que la contraseña actual sea la correcta
            if password_actual:
                if not self.instance.check_password(password_actual):
                    raise serializers.ValidationError({
                        "password_actual": "Contraseña incorrecta. No se pueden guardar los cambios."
                    })
            else:
                # Obligamos a React a siempre mandar la contraseña actual para editar
                raise serializers.ValidationError({
                    "password_actual": "Debes ingresar tu contraseña actual para autorizar los cambios."
                })

        # 3. Lógica para cuando mandan contraseñas nuevas (Registro o Cambio)
        if 'password' in data and 'confirm_password' in data:
            if data['password'] != data['confirm_password']:
                raise serializers.ValidationError({
                    "confirm_password": "Las contraseñas no coinciden. Por favor, verifica."
                })

        return data
    
    def update(self, instance, validated_data):
        # 4. Sobrescribimos cómo se guardan los datos al editar
        # Limpiamos los campos fantasma para que PostgreSQL no marque error
        validated_data.pop('confirm_password', None)
        validated_data.pop('password_actual', None)

        # Si el usuario aprovechó para cambiar su contraseña por una nueva, la encriptamos
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)

        # Guardamos el resto de los datos (nombre, correo, etc.)
        return super().update(instance, validated_data)

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
