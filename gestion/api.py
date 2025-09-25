from rest_framework import viewsets, permissions
from .models import Guardia, Secretaria, Administrador, Propietario
from .serializers import (
    GuardiaSerializer, 
    SecretariaSerializer, 
    AdministradorSerializer, 
    PropietarioSerializer
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