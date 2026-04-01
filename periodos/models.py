from django.db import models

class Periodo(models.Model):
    id_periodo = models.AutoField(primary_key=True)
    ciclo_escolar = models.CharField(max_length=50, help_text="Ejemplo: 2025-A")
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    # Usamos un Boolean para el estado: True = Activo, False = Inactivo
    estado = models.BooleanField(default=True) 

    class Meta:
        db_table = 'periodo'
        verbose_name_plural = 'Periodos'

    def __str__(self):
        return f"Ciclo {self.ciclo_escolar} - {'Activo' if self.estado else 'Inactivo'}"