from .models import Secretaria , PagoDespensa
from rest_framework import serializers

class SecretariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Secretaria
        fields = '__all__'

class PagoDespensaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PagoDespensa
        fields = '__all__'

