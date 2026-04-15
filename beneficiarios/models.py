from django.db import models
from django.conf import settings


class Direccion(models.Model):
    id_direccion = models.AutoField(primary_key=True)
    calle = models.CharField(max_length=50)
    numero = models.CharField(max_length=5)
    colonia = models.CharField(max_length=50)
    municipio = models.CharField(max_length=50)
    cp = models.CharField(max_length=5) # ejemplo 68000

    class Meta:
        db_table = 'direccion'
        verbose_name_plural = 'Direcciones'

    def __str__(self):
        return f"{self.calle} {self.numero}, {self.colonia}"


class Expediente(models.Model):
    id_expediente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20)
    apellido_p = models.CharField(max_length=15)
    apellido_m = models.CharField(max_length=15)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=10, null=True, blank=True)
    genero = models.CharField(max_length=15)
    correo = models.EmailField(max_length=30, null=True, blank=True)
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
    

class Postulante(models.Model):
    id_postulante = models.AutoField(primary_key=True)
    # Le ponemos un valor por defecto para que al crearlo siempre empiece en "Pendiente" o "En Revisión"
    estatus = models.CharField(max_length=50, default='Pendiente')
    
    # Relación con el Expediente
    id_expediente = models.ForeignKey(
        Expediente, 
        on_delete=models.CASCADE, # Si borran el expediente, se borra el postulante
        db_column='id_expediente',
        related_name='postulantes'
    )
    
    # Relación con el Usuario (Quien lo registró o le dará seguimiento)
    id_usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, # Si borran a la trabajadora social, el postulante no desaparece
        null=True, 
        db_column='id_usuario',
        related_name='postulantes_asignados'
    )

    class Meta:
        db_table = 'postulante'
        verbose_name_plural = 'Postulantes'

    def __str__(self):
        return f"Postulante {self.id_expediente.nombre} - {self.estatus}"


class Visita_Postulante(models.Model):
    id_visita = models.AutoField(primary_key=True)
    fecha_visita = models.DateTimeField() 
    estado_visita = models.CharField(max_length=50, default='Programada')
    nota_visita = models.TextField(null=True, blank=True)
    
    # Relación con el Postulante
    id_postulante = models.ForeignKey(
        Postulante, 
        on_delete=models.CASCADE, 
        db_column='id_postulante',
        related_name='visitas'
    )

    class Meta:
        db_table = 'visita_postulante'
        verbose_name_plural = 'Visitas de Postulantes'

    def __str__(self):
        return f"Visita a Postulante ID {self.id_postulante.id_postulante} - {self.fecha_visita}"
    
class Beneficiario(models.Model):
    id_beneficiario = models.AutoField(primary_key=True)
    estatus = models.CharField(max_length=20, default='Activo')
    notas = models.TextField(null=True, blank=True)
    fecha_ingreso = models.DateField(auto_now_add=True)
    
    id_expediente = models.ForeignKey(
        Expediente, 
        on_delete=models.CASCADE, 
        db_column='id_expediente',
        related_name='beneficiarios'
    )

    class Meta:
        db_table = 'beneficiario'
        verbose_name_plural = 'Beneficiarios'

    def __str__(self):
        return f"Beneficiario {self.id_expediente.nombre} - {self.estatus}"
    
class Fotografias(models.Model):
    id_foto = models.AutoField(primary_key=True)
    link = models.URLField(max_length=500) 
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    fecha_carga = models.DateField(auto_now_add=True)
    etapa = models.CharField(max_length=50) # Ej. Visita Domiciliaria, Seguimiento

    # Conexión 1 a MUCHOS con el expediente principal
    id_expediente = models.ForeignKey(
        Expediente, 
        on_delete=models.CASCADE, 
        db_column='id_expediente',
        related_name='fotografias'
    )

    class Meta:
        db_table = 'fotografias'