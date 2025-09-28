from django.db import models
from django.contrib.auth.models import User
from .enum import TIPO_USUARIO_CHOICES

# Create your models here.
class PerfilUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")

    tipo_usuario = models.CharField(
        max_length=20,
        choices=TIPO_USUARIO_CHOICES,
        default='POR_DESIGNAR',
    )
    imagen_perfil_url = models.URLField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    sexo = models.CharField(
        max_length=10,
        choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')],
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.user.username} ({self.get_tipo_usuario_display()})"
    
