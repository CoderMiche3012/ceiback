from django.db import models

class Direccion(models.Model):
    id_direccion = models.AutoField(primary_key=True)
    calle = models.CharField(max_length=255)
    numero = models.CharField(max_length=50)
    colonia = models.CharField(max_length=255)
    municipio = models.CharField(max_length=255)
    cp = models.CharField(max_length=10)

    class Meta:
        db_table = 'direccion'
        verbose_name_plural = 'Direcciones'

    def __str__(self):
        return f"{self.calle} {self.numero}, {self.colonia}"


class Expediente(models.Model):
    id_expediente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido_p = models.CharField(max_length=100)
    apellido_m = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=20, null=True, blank=True)
    genero = models.CharField(max_length=50)
    correo = models.EmailField(max_length=255, null=True, blank=True)
    nota_situacion_familiar = models.TextField(null=True, blank=True)
    
    id_direccion = models.ForeignKey(
        Direccion, 
        on_delete=models.SET_NULL, 
        null=True, 
        db_column='id_direccion',
        related_name='expedientes'
    )

    class Meta:
        db_table = 'expediente'
        verbose_name_plural = 'Expedientes'

    def __str__(self):
        return f"{self.nombre} {self.apellido_p} {self.apellido_m}"