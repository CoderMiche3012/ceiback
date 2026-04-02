from rest_framework import serializers
from django.core.validators import RegexValidator
from estudios.models import Estudio_Socioeconomico, Familia, Vivienda, Gastos, Alimentacion, Analisis

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

class EstudioSocioeconomicoSerializer(serializers.ModelSerializer):
    # Anidamos los componentes del estudio
    # Familiares es una lista (many=True), los demás son objetos únicos
    familiares = FamiliaSerializer(many=True, required=False)
    vivienda = ViviendaSerializer(required=False)
    gastos = GastosSerializer(required=False)
    alimentacion = AlimentacionSerializer(required=False)
    analisis = AnalisisSerializer(required=False)

    class Meta:
        model = Estudio_Socioeconomico
        fields = '__all__'

    def create(self, validated_data):
        # 1. Extraemos los diccionarios anidados del JSON
        familiares_data = validated_data.pop('familiares', [])
        vivienda_data = validated_data.pop('vivienda', None)
        gastos_data = validated_data.pop('gastos', None)
        alimentacion_data = validated_data.pop('alimentacion', None)
        analisis_data = validated_data.pop('analisis', None)

        # 2. Creamos el Estudio Principal
        estudio = Estudio_Socioeconomico.objects.create(**validated_data)

        # 3. Creamos los familiares (lista) conectándolos al Expediente
        for familiar in familiares_data:
            Familia.objects.create(id_expediente=estudio.id_expediente, **familiar)

        # 4. Creamos los satélites 1 a 1 conectándolos al Estudio que acabamos de crear
        if vivienda_data:
            Vivienda.objects.create(id_estudio=estudio, **vivienda_data)
        if gastos_data:
            Gastos.objects.create(id_estudio=estudio, **gastos_data)
        if alimentacion_data:
            Alimentacion.objects.create(id_estudio=estudio, **alimentacion_data)
        if analisis_data:
            Analisis.objects.create(id_estudio=estudio, **analisis_data)

        return estudio