from .serializers import * 
from rest_framework import viewsets , permissions
from .models import * 

class PropietarioViewSet(viewsets.ModelViewSet):
    queryset = Propietario.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = PropietarioSerializer

class QuejaViewSet(viewsets.ModelViewSet):
    queryset = Queja.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = QuejaSerializer

class MobilitadViewSet(viewsets.ModelViewSet):
    queryset = Mobilitad.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = MobilitadSerializer

class UnidadHabitacionalViewSet(viewsets.ModelViewSet):
    queryset = UnidadHabitacional.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UnidadHabitacionalSerializer

class PropietarioUnidadViewSet(viewsets.ModelViewSet):
    queryset = PropietarioUnidad.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = PropietarioUnidadSerializer

class AreaSocialViewSet(viewsets.ModelViewSet):
    queryset = AreaSocial.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = AreaSocialSerializer

class RegistroAreaSocialViewSet(viewsets.ModelViewSet):
    queryset = RegistroAreaSocial.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegistroAreaSocialSerializer 

