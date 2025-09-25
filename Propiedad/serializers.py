from rest_framework import serializers
from .models import UnidadHabitacional

class UnidadHabitacionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadHabitacional
        fields = '__all__'