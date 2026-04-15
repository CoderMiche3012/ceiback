from rest_framework import serializers
from django.core.validators import RegexValidator
from estudios.models import EstudioSocioeconomico, Familia, Analisis
from beneficiarios.models import Expediente

class AnalisisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analisis
        fields = '__all__'

class EstudioSocioeconomicoSerializer(serializers.ModelSerializer):
    analisis = AnalisisSerializer(read_only=True)

    class Meta:
        model = EstudioSocioeconomico
        fields = '__all__'

    def create(self, validated_data):
        estudio = EstudioSocioeconomico.objects.create(**validated_data)
        Analisis.objects.create(id_estudio=estudio, prioridad="Pendiente de evaluación")
        return estudio

class FamiliaSerializer(serializers.ModelSerializer):
    id_expediente = serializers.PrimaryKeyRelatedField(
        queryset=Expediente.objects.all(), 
        required=False
    )
    telefono_regex = RegexValidator(
        regex=r'^\d{10}$', 
        message="El número de teléfono debe contener exactamente 10 dígitos."
    )
    telefono = serializers.CharField(
        validators=[telefono_regex], 
        max_length=20, 
        required=False, 
        allow_null=True,
        allow_blank=True
    )

    class Meta:
        model = Familia
        fields = '__all__'

    def validate_edad(self, value):
        if value < 0 or value > 120:
            raise serializers.ValidationError("La edad debe ser un número lógico (entre 0 y 120 años).")
        return value

    def validate(self, data):
        actividad = data.get('actividad_principal', '').lower()
        salario = data.get('salario')

        if "estudiante" not in actividad and "hogar" not in actividad:
            if salario is None:
                raise serializers.ValidationError({
                    "salario": "Se requiere un salario si la actividad principal no es ser estudiante o labores del hogar."
                })
        
        return data