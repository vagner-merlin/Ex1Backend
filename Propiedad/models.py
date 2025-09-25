from django.db import models

from gestion.models import Propietario

# Create your models here.
class UnidadHabitacional(models.Model):
    # La clave foránea que apunta al Propietario
    propietario = models.ForeignKey(
        Propietario,
        on_delete=models.CASCADE,
        related_name='unidades_habitacionales'
    )
    residentes = models.TextField(verbose_name="Residentes")
    manzano = models.CharField(max_length=10, verbose_name="Manzano")
    lote = models.CharField(max_length=10, verbose_name="Lote")

    def __str__(self):
        return f"Manzano: {self.manzano}, Lote: {self.lote}"