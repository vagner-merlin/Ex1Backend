from django.db import models


class UnidadHabitacional(models.Model):
    # La clave foránea que apunta al Propietario
    propietario = models.ForeignKey(
        'gestion.Propietario',  # ✅ String reference
        on_delete=models.CASCADE,
        related_name='unidades_habitacionales'
    )
    residentes = models.TextField(verbose_name="Residentes")
    manzano = models.CharField(max_length=10, verbose_name="Manzano")
    lote = models.CharField(max_length=10, verbose_name="Lote")

    def __str__(self):
        return f"Manzano: {self.manzano}, Lote: {self.lote}"