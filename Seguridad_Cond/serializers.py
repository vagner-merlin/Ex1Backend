from .models import Guardia , Visita
from rest_framework import serializers

class GuardiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guardia
        fields = '__all__'

class VisitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visita
        fields = '__all__'

