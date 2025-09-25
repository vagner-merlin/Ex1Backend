from rest_framework import viewsets, permissions
from .models import Guardia, Secretaria, Administrador, Propietario, AreaSocial, ReservaArea, Visita, Queja, Deuda
from .serializers import (
    GuardiaSerializer, 
    SecretariaSerializer, 
    AdministradorSerializer, 
    PropietarioSerializer,
    AreaSocialSerializer,
    ReservaAreaSerializer,
    VisitaSerializer,
    QuejaSerializer,
    DeudaSerializer
)

# =================================================================
# ViewSets para CRUD completo - Sin autenticación
# =================================================================

class GuardiaViewSet(viewsets.ModelViewSet):
    queryset = Guardia.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = GuardiaSerializer

class SecretariaViewSet(viewsets.ModelViewSet):
    queryset = Secretaria.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = SecretariaSerializer

class AdministradorViewSet(viewsets.ModelViewSet):
    queryset = Administrador.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = AdministradorSerializer

class PropietarioViewSet(viewsets.ModelViewSet):
    queryset = Propietario.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = PropietarioSerializer

class AreaSocialViewSet(viewsets.ModelViewSet):
    queryset = AreaSocial.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = AreaSocialSerializer

class ReservaAreaViewSet(viewsets.ModelViewSet):
    queryset = ReservaArea.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ReservaAreaSerializer

class VisitaViewSet(viewsets.ModelViewSet):
    queryset = Visita.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = VisitaSerializer

class QuejaViewSet(viewsets.ModelViewSet):
    queryset = Queja.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = QuejaSerializer

class DeudaViewSet(viewsets.ModelViewSet):
    queryset = Deuda.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = DeudaSerializer