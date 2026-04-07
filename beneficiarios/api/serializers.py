from rest_framework import serializers
from django.core.validators import RegexValidator
from beneficiarios.models import Direccion, Expediente, Postulante, Visita_Postulante, Beneficiario, Fotografias

# --- Tus validadores se quedan igual ---
letras_regex = RegexValidator(regex=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', message='Solo letras y espacios.')
telefono_regex = RegexValidator(regex=r'^\d{10}$', message='Exactamente 10 dígitos.')
cp_regex = RegexValidator(regex=r'^\d{5}$', message='Exactamente 5 dígitos.')

class DireccionSerializer(serializers.ModelSerializer):
    cp = serializers.CharField(validators=[cp_regex])
    municipio = serializers.CharField(validators=[letras_regex])

    class Meta:
        model = Direccion
        fields = '__all__'

class ExpedienteSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(validators=[letras_regex])
    apellido_p = serializers.CharField(validators=[letras_regex])
    apellido_m = serializers.CharField(validators=[letras_regex])
    telefono = serializers.CharField(validators=[telefono_regex], required=False, allow_blank=True, allow_null=True)
    
    # Declaramos que la dirección vendrá anidada dentro del expediente
    id_direccion = DireccionSerializer()

    class Meta:
        model = Expediente
        # Ojo: Quitamos 'id_direccion' y ponemos 'direccion' (el objeto anidado)
        fields = ['nombre', 'apellido_p', 'apellido_m', 'fecha_nacimiento', 'telefono', 'genero', 'correo', 'nota_situacion_familiar', 'id_direccion']

class PostulanteSerializer(serializers.ModelSerializer):
    # Declaramos que el expediente vendrá anidado dentro del postulante
    id_expediente = ExpedienteSerializer()

    class Meta:
        model = Postulante
        fields = ['id_postulante', 'estatus', 'id_usuario', 'id_expediente']

    # ¡Aquí interceptamos el JSON antes de que toque la base de datos!
    def create(self, validated_data):
            # Actualizamos las llaves que sacamos del JSON
            expediente_data = validated_data.pop('id_expediente')
            direccion_data = expediente_data.pop('id_direccion')

            # Creamos de adentro hacia afuera
            direccion_obj = Direccion.objects.create(**direccion_data)
            expediente_obj = Expediente.objects.create(id_direccion=direccion_obj, **expediente_data)
            postulante_obj = Postulante.objects.create(id_expediente=expediente_obj, **validated_data)

            return postulante_obj

class VisitaPostulanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visita_Postulante
        fields = '__all__'

class BeneficiarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beneficiario
        fields = '__all__'

class FotografiasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fotografias
        fields = '__all__'


class ExpedienteSerializer(serializers.ModelSerializer):
    # 1. Declaramos un campo calculado dinámico
    familiares = serializers.SerializerMethodField()

    class Meta:
        model = Expediente
        fields = '__all__'

    # 2. Esta función va y busca a la familia en la otra app
    def get_familiares(self, obj):
        # Importamos aquí adentro para que Django no se confunda cruzando apps
        from estudios.models import Familia
        from estudios.api.serializers import FamiliaSerializer
        
        # Filtramos la familia que tenga el ID de este expediente
        familiares_vinculados = Familia.objects.filter(id_expediente=obj.id_expediente)
        
        # Devolvemos la lista serializada
        return FamiliaSerializer(familiares_vinculados, many=True).data
    
    fotografias = FotografiasSerializer(many=True, read_only=True)

    class Meta:
        model = Expediente
        fields = '__all__'