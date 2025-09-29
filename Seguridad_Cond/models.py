from django.db import models
from user_Cond.models import PerfilUser
from .enum import TURNO
from Propietarios_Cond.models import Propietario, UnidadHabitacional

# Create your models here.
class Guardia(models.Model):
    perfil = models.OneToOneField(
        PerfilUser, 
        on_delete=models.CASCADE, 
        primary_key=True,
        related_name="datos_guardia"  # ✅ CAMBIAR: datos_propietario → datos_guardia
    )
    turno = models.CharField(
        max_length=20,
        choices=TURNO,
        default='MAÑANA',
    )
    is_activo = models.BooleanField(default=True)
    fecha_contratacion = models.DateField(auto_now_add=True)
    informacion_adicional = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Guardia: {self.perfil.user.username} - {self.turno}"

class Visita(models.Model):
    placa_vehiculo = models.CharField(max_length=20, blank=True, null=True)
    descripcion = models.TextField()
    UnidadHabitacional = models.ForeignKey(
        UnidadHabitacional, 
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Visita a {self.UnidadHabitacional}"
