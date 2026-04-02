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

class Vivienda(models.Model):
    id_vivienda = models.AutoField(primary_key=True)
    tenencia = models.CharField(max_length=15) # Ej. Propia, Rentada, Prestada, Irregular
    material_techo = models.CharField(max_length=15) # Ej. Losa, Lámina, Asbesto
    material_piso = models.CharField(max_length=15)  # Ej. Cemento, Tierra, Mosaico
    material_muros = models.CharField(max_length=15) # Ej. Block, Ladrillo, Adobe, Madera
    num_cuartos = models.IntegerField()
    num_dormitorios = models.IntegerField()
    
    # Servicios básicos
    tiene_agua = models.BooleanField(default=False)
    tiene_luz = models.BooleanField(default=False)
    tiene_drenaje = models.BooleanField(default=False)
    tiene_internet = models.BooleanField(default=False)

    # Conexión 1 a 1 con el estudio principal
    id_estudio = models.OneToOneField(
        Estudio_Socioeconomico, 
        on_delete=models.CASCADE, 
        db_column='id_estudio',
        related_name='vivienda'
    )

    class Meta:
        db_table = 'vivienda'
        verbose_name_plural = 'Viviendas'

    def __str__(self):
        return f"Vivienda del Estudio {self.id_estudio.id_estudio}"


class Gastos(models.Model):
    id_gasto = models.AutoField(primary_key=True)
    # Usamos DecimalField para todo lo que sea dinero
    alimentacion = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    luz = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    agua = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    renta = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    educacion = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    transporte = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    salud = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    otros_gastos = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    id_estudio = models.OneToOneField(
        Estudio_Socioeconomico, 
        on_delete=models.CASCADE, 
        db_column='id_estudio',
        related_name='gastos'
    )

    class Meta:
        db_table = 'gastos'
        verbose_name_plural = 'Gastos'

    def __str__(self):
        return f"Gastos del Estudio {self.id_estudio.id_estudio}"


class Alimentacion(models.Model):
    id_alimentacion = models.AutoField(primary_key=True)
    # Frecuencia medida en días a la semana (0 a 7)
    frecuencia_carne = models.IntegerField(default=0)
    frecuencia_leche = models.IntegerField(default=0)
    frecuencia_huevo = models.IntegerField(default=0)
    frecuencia_frutas = models.IntegerField(default=0)
    frecuencia_verduras = models.IntegerField(default=0)
    frecuencia_cereales = models.IntegerField(default=0)

    id_estudio = models.OneToOneField(
        Estudio_Socioeconomico, 
        on_delete=models.CASCADE, 
        db_column='id_estudio',
        related_name='alimentacion'
    )

    class Meta:
        db_table = 'alimentacion'
        verbose_name_plural = 'Alimentación'


class Analisis(models.Model):
    id_analisis = models.AutoField(primary_key=True)
    diagnostico_social = models.TextField()
    sugerencia_apoyo = models.TextField()
    viabilidad = models.CharField(max_length=15) # Ej. Alta, Media, Baja, Rechazado
    fecha_analisis = models.DateField(auto_now_add=True)

    id_estudio = models.OneToOneField(
        Estudio_Socioeconomico, 
        on_delete=models.CASCADE, 
        db_column='id_estudio',
        related_name='analisis'
    )

    class Meta:
        db_table = 'analisis'
        verbose_name_plural = 'Análisis'