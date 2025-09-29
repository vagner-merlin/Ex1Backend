from .serializers import SecretariaSerializer , PagoDespensaSerializer
from rest_framework import viewsets , permissions 
from .models import Secretaria , PagoDespensa

class SecretariaViewSet(viewsets.ModelViewSet):
    queryset = Secretaria.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = SecretariaSerializer

class PagoDespensaViewSet(viewsets.ModelViewSet):
    queryset = PagoDespensa.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = PagoDespensaSerializer