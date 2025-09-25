from rest_framework import viewsets, permissions
from .models import UnidadHabitacional
from .serializers import UnidadHabitacionalSerializer

class UnidadHabitacionalViewSet(viewsets.ModelViewSet):
    queryset = UnidadHabitacional.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UnidadHabitacionalSerializer