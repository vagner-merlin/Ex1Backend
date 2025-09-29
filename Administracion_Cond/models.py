from django.db import models
from user_Cond.models import PerfilUser
# Create your models here.
from Seguridad_Cond.enum import TURNO
from Propietarios_Cond.models import UnidadHabitacional , Propietario


class Secretaria(models.Model):
    perfil = models.OneToOneField(
        PerfilUser, 
        on_delete=models.CASCADE, 
        primary_key=True,
        related_name="datos_secretaria"  
    )
    turno = models.CharField(
        max_length=20,
        choices=TURNO,
        default='MAÑANA',
    )
    velocidad_teclado = models.IntegerField(default=40)
    

class PagoDespensa(models.Model):
    fechade_pago = models.DateField()
    monto = models.FloatField()
    UnidadH = models.ForeignKey(
        UnidadHabitacional, 
        on_delete=models.CASCADE,
        related_name="pagos_despensa"
    )
    propietario = models.ForeignKey(
        Propietario, 
        on_delete=models.CASCADE,
        related_name="pagos_despensa"
    )
    is_principal = models.BooleanField(default=True)
    descripcion = models.TextField(blank=True, null=True)
    
