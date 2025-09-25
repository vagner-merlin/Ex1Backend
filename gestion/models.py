import random
import string
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver



#creacmos enum 
TURNO_CHOICES = [
    ('MANANA', 'Mañana'),
    ('TARDE', 'Tarde'),
    ('NOCHE', 'Noche'),
]

class Guardia(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    turno = models.CharField(
        max_length=6,
        choices=TURNO_CHOICES,
        default='MANANA',
        verbose_name="Turno de Servicio"
    )

    def __str__(self):
        return f"{self.user.username} - {self.created.strftime('%Y-%m-%d')} - {self.turno}"




class Secretaria(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    turno = models.CharField(
        max_length=6,
        choices=TURNO_CHOICES,
        default='MANANA',
        verbose_name="Turno de Servicio"
    )


class Administrador(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    cargo = models.CharField(max_length=100, verbose_name="Cargo del Administrador")



class Propietario(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    codigo_propietario = models.CharField(
            max_length=20,
            unique=True,
            blank=True,  # Permite que el campo esté vacío
            verbose_name="Código de Propietario"
        )
    
    def __str__(self):
        return f"Propietario: {self.codigo_propietario}"
    
#creacion de codigo por defecto 
def generate_unique_code():
    # Genera un código aleatorio de 4 dígitos
    return ''.join(random.choices(string.digits, k=4))

@receiver(pre_save, sender=Propietario)
def set_propietario_code(sender, instance, **kwargs):
    # Solo genera el código si el objeto es nuevo
    if not instance.pk:
        new_code = f"CON-{generate_unique_code()}"
        # Asegura que el código sea único antes de asignarlo
        while Propietario.objects.filter(codigo_propietario=new_code).exists():
            new_code = f"CON-{generate_unique_code()}"
        instance.codigo_propietario = new_code

