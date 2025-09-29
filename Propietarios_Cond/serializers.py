from .models import Propietario , Queja , Mobilitad , UnidadHabitacional , PropietarioUnidad ,AreaSocial ,  RegistroAreaSocial
from rest_framework import serializers

class PropietarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Propietario
        fields = '__all__'

class QuejaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Queja
        fields = '__all__'

class MobilitadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mobilitad
        fields = '__all__'

class UnidadHabitacionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadHabitacional
        fields = '__all__'

class PropietarioUnidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropietarioUnidad
        fields = '__all__'

class AreaSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaSocial
        fields = '__all__'

class RegistroAreaSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroAreaSocial
        fields = '__all__'

