from rest_framework import serializers , viewsets , permissions
from .serializers import UserSerializer, GroupSerializer
from django.contrib.auth.models import User, Group
from .models import PerfilUser
from .serializers import PerfilUserSerializer

class UserViewSet(viewsets.ModelViewSet):  
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet): 
    queryset = Group.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = GroupSerializer

class PerfilUserViewSet(viewsets.ModelViewSet):
    queryset = PerfilUser.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = PerfilUserSerializer
    