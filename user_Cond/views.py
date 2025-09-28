from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.db import transaction
from .models import PerfilUser

# =================================================================
# REGISTER - Crear usuario y perfil en una sola operación
# =================================================================
@api_view(['POST'])
def Register(request):
    """
    Registro que crea User y PerfilUser simultáneamente
    """
    try:
        with transaction.atomic():
            # DATOS PARA AUTH_USER
            username = request.data.get('username')
            email = request.data.get('email')
            password = request.data.get('password')
            last_name = request.data.get('last_name', '')
            first_name = request.data.get('first_name', '')
            
            # DATOS PARA PERFILUSER
            tipo_usuario = request.data.get('tipo_usuario', 'POR_DESIGNAR')
            telefono = request.data.get('telefono', '')
            direccion = request.data.get('direccion', '')
            sexo = request.data.get('sexo', '')
            imagen_perfil_url = request.data.get('imagen_perfil_url', '')
            
            # VALIDACIONES BÁSICAS
            if not username or not email or not password:
                return Response({
                    'error': 'Username, email and password are required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Verificar si el usuario ya existe
            if User.objects.filter(username=username).exists():
                return Response({
                    'error': 'Username already exists'
                }, status=status.HTTP_400_BAD_REQUEST)
                
            if User.objects.filter(email=email).exists():
                return Response({
                    'error': 'Email already exists'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # LÓGICA DE PERMISOS SEGÚN TIPO DE USUARIO
            is_superuser = (tipo_usuario == 'ADMINISTRADOR')
            is_staff = (tipo_usuario == 'ADMINISTRADOR')
            
            # CREAR USUARIO EN AUTH_USER
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_superuser=is_superuser,
                is_staff=is_staff,
                is_active=True
            )
            
            print(f"✅ Usuario creado: ID={user.id}, Username={user.username}, Tipo={tipo_usuario}")
            
            # CREAR PERFIL DE USUARIO
            perfil_user = PerfilUser.objects.create(
                user=user,  # FK al usuario recién creado
                tipo_usuario=tipo_usuario,
                telefono=telefono,
                direccion=direccion,
                sexo=sexo if sexo in ['M', 'F', 'O'] else None,
                imagen_perfil_url=imagen_perfil_url if imagen_perfil_url else None
            )
            
            print(f"✅ PerfilUser creado: ID={perfil_user.id}, Tipo={perfil_user.tipo_usuario}")
            
            # CREAR TOKEN PARA AUTENTICACIÓN INMEDIATA
            token = Token.objects.create(user=user)
            
            return Response({
                "message": "Registration successful",
                "token": token.key,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "is_superuser": user.is_superuser,
                    "is_staff": user.is_staff
                },
                "perfil": {
                    "id": perfil_user.id,
                    "tipo_usuario": perfil_user.tipo_usuario,
                    "tipo_usuario_display": perfil_user.get_tipo_usuario_display(),
                    "telefono": perfil_user.telefono,
                    "direccion": perfil_user.direccion,
                    "sexo": perfil_user.sexo,
                    "imagen_perfil_url": perfil_user.imagen_perfil_url
                }
            }, status=status.HTTP_201_CREATED)
            
    except Exception as e:
        print(f"❌ Error en registro: {str(e)}")
        return Response({
            'error': 'Registration failed', 
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# =================================================================
# LOGIN - Con email y password, devuelve tipo de usuario
# =================================================================
@api_view(['POST'])
def Login(request):
    """
    Login con email y password - Devuelve tipo de usuario del enum
    """
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response({
            "error": "Email and password are required"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Buscar usuario por email
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({
            "error": "User with this email does not exist"
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Verificar password
    if not user.check_password(password):
        return Response({
            "error": "Invalid password"
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    # Verificar si está activo
    if not user.is_active:
        return Response({
            "error": "User account is disabled"
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        # Obtener perfil del usuario para tipo de usuario
        perfil_user = PerfilUser.objects.get(user=user)
    except PerfilUser.DoesNotExist:
        return Response({
            "error": "User profile not found"
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Obtener o crear token
    token, created = Token.objects.get_or_create(user=user)
    
    return Response({
        "message": "Login successful",
        "token": token.key,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_superuser": user.is_superuser,
            "is_staff": user.is_staff
        },
        "perfil": {
            "id": perfil_user.id,
            "tipo_usuario": perfil_user.tipo_usuario,
            "tipo_usuario_display": perfil_user.get_tipo_usuario_display(),
            "telefono": perfil_user.telefono,
            "direccion": perfil_user.direccion,
            "sexo": perfil_user.sexo,
            "imagen_perfil_url": perfil_user.imagen_perfil_url
        }
    }, status=status.HTTP_200_OK)

# =================================================================
# PROFILE - Obtener perfil completo (requiere token)
# =================================================================
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Profile(request):
    """
    Perfil completo del usuario autenticado
    """
    user = request.user
    
    try:
        # Obtener el perfil del usuario
        perfil_user = PerfilUser.objects.get(user=user)
        
        # Obtener grupos del usuario
        user_groups = user.groups.all()
        groups_data = [{"id": group.id, "name": group.name} for group in user_groups]
        
        return Response({
            "message": f"Perfil de usuario: {user.username}",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "is_superuser": user.is_superuser,
                "is_staff": user.is_staff,
                "is_active": user.is_active,
                "date_joined": user.date_joined,
                "last_login": user.last_login
            },
            "perfil": {
                "id": perfil_user.id,
                "tipo_usuario": perfil_user.tipo_usuario,
                "tipo_usuario_display": perfil_user.get_tipo_usuario_display(),
                "telefono": perfil_user.telefono,
                "direccion": perfil_user.direccion,
                "sexo": perfil_user.sexo,
                "imagen_perfil_url": perfil_user.imagen_perfil_url
            },
            "groups": groups_data,
            "permissions": {
                "is_admin": user.is_superuser,
                "can_access_admin": user.is_staff,
                "user_type": perfil_user.tipo_usuario
            },
            "status": "authenticated"
        }, status=status.HTTP_200_OK)
        
    except PerfilUser.DoesNotExist:
        return Response({
            "error": "User profile not found",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_superuser": user.is_superuser
            }
        }, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({
            "error": "Error retrieving profile",
            "details": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# =================================================================
# LOGOUT - Eliminar token
# =================================================================
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Logout(request):
    """
    Logout del usuario - elimina el token
    """
    try:
        # Eliminar el token del usuario
        token = Token.objects.get(user=request.user)
        token.delete()
        
        return Response({
            "message": "Logout successful",
            "status": "logged_out"
        }, status=status.HTTP_200_OK)
        
    except Token.DoesNotExist:
        return Response({
            "message": "User was already logged out",
            "status": "logged_out"
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({
            "error": "Error during logout",
            "details": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
