from django.db import models
# ¡Aquí está la magia! Importamos el modelo desde tu otra app
from beneficiarios.models import Expediente 

class Estudio_Socioeconomico(models.Model):
    id_estudio = models.AutoField(primary_key=True)
    nivel_escolar_inicial = models.CharField(max_length=25)
    grado_escolar_inicial = models.CharField(max_length=15)
    referencia_ingreso = models.CharField(max_length=255, null=True, blank=True)
    tipo_comida_en_casa = models.CharField(max_length=255, null=True, blank=True)
    estatus_estudio = models.CharField(max_length=50, default='En proceso')
    
    # Llave foránea que conecta con el Expediente de la otra app
    id_expediente = models.ForeignKey(
        Expediente, 
        on_delete=models.CASCADE, 
        db_column='id_expediente',
        related_name='estudios_socioeconomicos'
    )

    class Meta:
        db_table = 'estudio_socioeconomico'
        verbose_name_plural = 'Estudios Socioeconómicos'

    def __str__(self):
        return f"Estudio de {self.id_expediente.nombre} - {self.estatus_estudio}"


class Familia(models.Model):
    id_familia = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=25)
    apellido_p = models.CharField(max_length=25)
    apellido_m = models.CharField(max_length=25)
    parentesco = models.CharField(max_length=50)
    edad = models.IntegerField()
    actividad_principal = models.CharField(max_length=100)
    area_laboral_escuela = models.CharField(max_length=100, null=True, blank=True)
    # Usamos DecimalField para manejar dinero (max_digits=10 permite hasta 99,999,999.99)
    salario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    vive_en_casa = models.BooleanField(default=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    es_tutor_principal = models.BooleanField(default=False)
    
    # Según tu diagrama, Familia también se conecta directo al Expediente
    id_expediente = models.ForeignKey(
        Expediente, 
        on_delete=models.CASCADE, 
        db_column='id_expediente',
        related_name='familiares'
    )

    class Meta:
        db_table = 'familia'
        verbose_name_plural = 'Familiares'

    def __str__(self):
        return f"{self.nombre} ({self.parentesco})"