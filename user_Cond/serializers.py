from rest_framework import serializers
from django.contrib.auth.models import User, Group 
from .models import PerfilUser

class UserSerializer(serializers.ModelSerializer):  
    class Meta:
        model = User 
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
    
class PerfilUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilUser
        fields = '__all__'
