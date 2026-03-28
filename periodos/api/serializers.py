from rest_framework import serializers
from periodos.models import Periodo

class PeriodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Periodo
        fields = '__all__' # Queremos que el frontend mande y reciba todos los campos