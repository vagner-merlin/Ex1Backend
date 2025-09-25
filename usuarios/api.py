from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets , permissions

@api_view(['POST'])
def Register(request):
    usernew = UserSerializer(data = request.data)
    
    if usernew.is_valid():
        usernew.save()

        user = User.objects.get(username = usernew.data['username'])
        user.set_password(request.data['password'])
        user.save()

        token = Token.objects.create(user = user)
        return Response({"token": token.key , "user": usernew.data}, status = status.HTTP_201_CREATED)
        
    return Response( usernew.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def Login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)
    
    user = get_object_or_404(User, email=email)
    
    if not user.check_password(password):
        return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
    
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    
    return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_200_OK)
    

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Profile(request):
    user = request.user
    serializer = UserSerializer(instance=user)
    
    return Response({
        "message": f"Usted está logueado con el usuario: {user.username}",
        "user": serializer.data,
        "status": "authenticated"
    }, status=status.HTTP_200_OK)

#---------------------------------------------------------

#creacion de crud 
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer