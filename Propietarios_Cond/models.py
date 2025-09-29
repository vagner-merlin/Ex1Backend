from django.db import models
from user_Cond.models import PerfilUser
from .enum import ESTADO
# Create your models here.

class Propietario(models.Model):
    perfil = models.OneToOneField(
        PerfilUser, 
        on_delete=models.CASCADE, 
        primary_key=True,
        related_name="datos_propietario" # Nombre más específico para evitar conflictos
    )
    is_activo = models.BooleanField(default=True)
    codigo_propietario = models.CharField(max_length=20, unique=True)
    

class Queja(models.Model):
    propietarios = models.ForeignKey(
        Propietario, 
        on_delete=models.CASCADE, 
        related_name="quejas"
    )
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=20,
        choices=ESTADO,
        default='EN_PROCESO',
    )

class Mobilitad (models.Model):
    propietarios = models.ForeignKey(
        Propietario, 
        on_delete=models.CASCADE, 
        related_name="mobilidades"
    )
    descripcion = models.TextField()
    imangen_url = models.URLField(blank=True, null=True)


class UnidadHabitacional(models.Model):
    Descripcion = models.CharField(max_length=100)
    piso = models.IntegerField()

class PropietarioUnidad(models.Model):
    propietario = models.ForeignKey(
        Propietario , 
        on_delete=models.CASCADE,
        related_name='posesiones'
    )
    unidad_habitacional = models.ForeignKey(
        UnidadHabitacional, 
        on_delete=models.CASCADE,
        related_name='propietarios'
    )
    is_principal = models.BooleanField(default=False)

class AreaSocial(models.Model):
    descripcion = models.CharField(max_length=100)

class RegistroAreaSocial(models.Model):
    fecha_reserva = models.DateTimeField()
    descripcion = models.TextField()
    AreaSocial = models.ForeignKey(
        AreaSocial, 
        on_delete=models.CASCADE,
        related_name='registros'
    )
    is_principal = models.BooleanField(default=False)