from rest_framework import serializers
from django.core.validators import RegexValidator
from estudios.models import Estudio_Socioeconomico, Familia, Vivienda, Gastos, Alimentacion, Analisis, Situacion_Familiar, Servicios_Vivienda, Sugerencias

#VALIDACIONES 
letras_regex = RegexValidator(
    regex=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', 
    message='El nombre solo debe contener letras y espacios.'
)
telefono_regex = RegexValidator(
    regex=r'^\d{10}$', 
    message='El teléfono debe contener exactamente 10 dígitos.'
)

class FamiliaSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(validators=[letras_regex])
    # El teléfono puede venir vacío si el familiar no tiene, pero si trae algo, deben ser 10 números
    telefono = serializers.CharField(
        validators=[telefono_regex], 
        required=False, 
        allow_blank=True, 
        allow_null=True
    )

    class Meta:
        model = Familia
        exclude = ['id_expediente']

class ViviendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vivienda
        exclude = ['id_estudio'] # Se lo inyectaremos en el backend

class GastosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gastos
        exclude = ['id_estudio']

class AlimentacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alimentacion
        exclude = ['id_estudio']

class AnalisisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analisis
        exclude = ['id_estudio']

class SituacionFamiliarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Situacion_Familiar
        exclude = ['id_estudio']

class ServiciosViviendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicios_Vivienda
        exclude = ['id_estudio']

class SugerenciasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sugerencias
        exclude = ['id_estudio']

class EstudioSocioeconomicoSerializer(serializers.ModelSerializer):
    # 1. Anidamos todos los componentes (incluyendo los 3 nuevos)
    familiares = FamiliaSerializer(many=True, required=False)
    vivienda = ViviendaSerializer(required=False)
    gastos = GastosSerializer(required=False)
    alimentacion = AlimentacionSerializer(required=False)
    analisis = AnalisisSerializer(required=False)
    situacion_familiar = SituacionFamiliarSerializer(required=False) 
    servicios_vivienda = ServiciosViviendaSerializer(required=False)
    sugerencias = SugerenciasSerializer(required=False)

    class Meta:
        model = Estudio_Socioeconomico
        fields = '__all__'

    def create(self, validated_data):
        # 2. Extraemos TODOS los diccionarios anidados del JSON (El orden no importa, pero no debe faltar ninguno)
        familiares_data = validated_data.pop('familiares', [])
        vivienda_data = validated_data.pop('vivienda', None)
        gastos_data = validated_data.pop('gastos', None)
        alimentacion_data = validated_data.pop('alimentacion', None)
        analisis_data = validated_data.pop('analisis', None)
        situacion_familiar_data = validated_data.pop('situacion_familiar', None)
        servicios_vivienda_data = validated_data.pop('servicios_vivienda', None)
        sugerencias_data = validated_data.pop('sugerencias', None)

        # 3. Creamos el Estudio Principal
        estudio = Estudio_Socioeconomico.objects.create(**validated_data)

        # 4. Creamos los familiares (lista) conectándolos al Expediente
        for familiar in familiares_data:
            Familia.objects.create(id_expediente=estudio.id_expediente, **familiar)

        # 5. Creamos TODOS los satélites 1 a 1 conectándolos al Estudio que acabamos de crear
        if vivienda_data:
            Vivienda.objects.create(id_estudio=estudio, **vivienda_data)
        if gastos_data:
            Gastos.objects.create(id_estudio=estudio, **gastos_data)
        if alimentacion_data:
            Alimentacion.objects.create(id_estudio=estudio, **alimentacion_data)
        if analisis_data:
            Analisis.objects.create(id_estudio=estudio, **analisis_data)
        if situacion_familiar_data:
            Situacion_Familiar.objects.create(id_estudio=estudio, **situacion_familiar_data)
        if servicios_vivienda_data:
            Servicios_Vivienda.objects.create(id_estudio=estudio, **servicios_vivienda_data)
        if sugerencias_data:
            Sugerencias.objects.create(id_estudio=estudio, **sugerencias_data)

        return estudio
    
class ServiciosViviendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicios_Vivienda
        exclude = ['id_estudio']

class SugerenciasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sugerencias
        exclude = ['id_estudio']