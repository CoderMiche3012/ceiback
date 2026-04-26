from rest_framework import serializers
from django.core.validators import RegexValidator
from donadores.models import Donador, DonativoDonador
from beneficiarios.models import Beneficiario

letras_regex = RegexValidator(regex=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s.,&]+$', message='Solo letras, espacios y puntuación básica.')
telefono_regex = RegexValidator(regex=r'^\d{10}$', message='El numero telefonico lleva 10 digitos')
cp_regex = RegexValidator(regex=r'^\d{5}$', message='El cp lleva 5 digitos')

class DonadorSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(validators=[letras_regex])
    telefono = serializers.CharField(validators=[telefono_regex], required=False, allow_blank=True, allow_null=True)
    cp = serializers.CharField(validators=[cp_regex], required=False, allow_blank=True, allow_null=True)
    
    beneficiarios_apoyados = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Beneficiario.objects.all(),
        required=False
    )

    class Meta:
        model = Donador
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)

        response['nombres_beneficiarios'] = [
            f"{b.id_expediente.nombre} {b.id_expediente.apellido_p}" 
            for b in instance.beneficiarios_apoyados.all()
        ]
        return response


class DonativoDonadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonativoDonador
        fields = '__all__'

    def validate_monto(self, value):
        if value <= 0:
            raise serializers.ValidationError("El monto del donativo debe ser mayor a cero.")
        return value