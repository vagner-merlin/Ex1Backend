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

ESTADO_RESERVA_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('APROBADA', 'Aprobada'),
        ('RECHAZADA', 'Rechazada'),
        ('CANCELADA', 'Cancelada'),
        ('FINALIZADA', 'Finalizada'),
    ]

ESTADO_QUEJA_CHOICES = [
    ('ABIERTA', 'Abierta'),
    ('PROCESO', 'En Proceso'),
    ('CERRADA', 'Cerrada'),
    ('RESUELTA', 'Resuelta'),
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
        
        return f"{self.user.username} - {self.turno}"




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

#----------------------------------------------------------------
#area sociales 

class AreaSocial(models.Model):
    nombre = models.CharField(
        max_length=100, 
        unique=True, 
        verbose_name="Nombre del Área"
    )
    capacidad_maxima = models.IntegerField(
        verbose_name="Capacidad Máxima"
    )
    costo_por_hora = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Costo por Hora"
    )
    reglamento = models.TextField(
        verbose_name="Reglamento del Área"
    )

    def __str__(self):
        return self.nombre
    
class ReservaArea(models.Model):
    propietario = models.ForeignKey(
        Propietario,  
        on_delete=models.CASCADE,
        related_name='reservas_propietario'
    )
    area_social = models.ForeignKey(
        AreaSocial, 
        on_delete=models.CASCADE,
        related_name='reservas_area'
    )
    fecha_reserva = models.DateField(verbose_name="Fecha de Reserva")
    hora_inicio = models.TimeField(verbose_name="Hora de Inicio")
    hora_fin = models.TimeField(verbose_name="Hora de Fin")
    estado = models.CharField(
        max_length=10, 
        choices=ESTADO_RESERVA_CHOICES,
        default='PENDIENTE',
        verbose_name="Estado de la Reserva"
    )



    

class Visita(models.Model):
    guardia = models.ForeignKey(
        Guardia,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='visitas_registradas'
    )
    unidad_habitacional = models.ForeignKey(
        'Propiedad.UnidadHabitacional',  # ✅ String reference
        on_delete=models.CASCADE,
        related_name='visitas_unidad'
    )
    fecha_hora_entrada = models.DateTimeField(verbose_name="Fecha y Hora de Entrada")
    fecha_hora_salida = models.DateTimeField(null=True, blank=True, verbose_name="Fecha y Hora de Salida")
    nombre_visitante = models.CharField(max_length=100, verbose_name="Nombre del Visitante")
    ci_visitante = models.CharField(max_length=20, verbose_name="CI del Visitante")
    placa_vehiculo = models.CharField(max_length=20, blank=True, verbose_name="Placa del Vehículo")

    def __str__(self):
        return f"Visita de {self.nombre_visitante} - {self.fecha_hora_entrada.strftime('%Y-%m-%d %H:%M')}"
    
class Queja(models.Model):
    propietario = models.ForeignKey(
        Propietario,
        on_delete=models.CASCADE,
        related_name='quejas_reportadas'
    )
    unidad_habitacional = models.ForeignKey(
        'Propiedad.UnidadHabitacional',  # ✅ String reference
        on_delete=models.CASCADE,
        related_name='quejas_unidad'
    )
    titulo = models.CharField(max_length=200, verbose_name="Título de la Queja")
    descripcion = models.TextField(verbose_name="Descripción")
    estado = models.CharField(
        max_length=10,
        choices=ESTADO_QUEJA_CHOICES,
        default='ABIERTA',
        verbose_name="Estado de la Queja"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):  # ✅ Corregí __str__ (no _str_)
        return f"{self.titulo} - {self.get_estado_display()} ({self.propietario.user.username})"
    
class Deuda(models.Model):
    unidad_habitacional = models.ForeignKey(
        'Propiedad.UnidadHabitacional',  # ✅ String reference
        on_delete=models.CASCADE,
        related_name='deudas_unidad'
    )
    monto = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto de la Deuda")
    fecha_vencimiento = models.DateField(verbose_name="Fecha de Vencimiento")
    pagada = models.BooleanField(default=False, verbose_name="¿Está pagada?")
    fecha_pago = models.DateField(null=True, blank=True, verbose_name="Fecha de Pago")

    def __str__(self):  # ✅ Corregí __str__ (no _str_)
        estado = "Pagada" if self.pagada else "Pendiente"
        return f"Deuda de {self.monto} - {estado}"