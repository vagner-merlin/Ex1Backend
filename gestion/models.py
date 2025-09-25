from django.db import models
from django.contrib.auth.models import User


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
    created = models.DateTimeField(auto_now_add=True)
    turno = models.CharField(
        max_length=6,
        choices=TURNO_CHOICES,
        default='MANANA',
        verbose_name="Turno de Servicio"
    )

    def __str__(self):
        return f"{self.user.username} - {self.created.strftime('%Y-%m-%d')} - {self.turno}"
