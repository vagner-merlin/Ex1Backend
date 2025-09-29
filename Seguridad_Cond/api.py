from rest_framework import viewsets , permissions
from .models import Guardia, Visita
from .serializers import GuardiaSerializer, VisitaSerializer

class GuardiaViewSet(viewsets.ModelViewSet):
    queryset = Guardia.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = GuardiaSerializer
        

class VisitaViewSet(viewsets.ModelViewSet):
    queryset = Visita.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = VisitaSerializer