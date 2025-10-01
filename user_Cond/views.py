from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token  # ✅ Import correcto
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
            token = Token.objects.create(user=user)  # ✅ Ahora debería funcionar
            
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

# =================================================================
# REGISTER SECRETARIA - Crear User + PerfilUser + Secretaria
# =================================================================
@api_view(['POST'])
def RegisterSecretaria(request):
    """
    Registro específico para Secretarias - Crea User, PerfilUser y Secretaria automáticamente
    """
    try:
        with transaction.atomic():
            # DATOS PARA AUTH_USER
            username = request.data.get('username')
            email = request.data.get('email')
            password = request.data.get('password')
            first_name = request.data.get('first_name', '')
            last_name = request.data.get('last_name', '')
            
            # DATOS PARA PERFILUSER
            telefono = request.data.get('telefono', '')
            direccion = request.data.get('direccion', '')
            sexo = request.data.get('sexo', '')
            
            # DATOS PARA SECRETARIA
            turno = request.data.get('turno', 'MAÑANA')  # Default MAÑANA
            velocidad_teclado = request.data.get('velocidad_teclado', 40)  # Default 40
            
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
            
            # PASO 1: CREAR USUARIO EN AUTH_USER
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_superuser=False,  # Secretaria no es superuser
                is_staff=True,       # Secretaria tiene acceso administrativo
                is_active=True
            )
            
            print(f"✅ Usuario creado: ID={user.id}, Username={user.username}")
            
            # PASO 2: CREAR PERFIL DE USUARIO (tipo_usuario = SECRETARIA)
            perfil_user = PerfilUser.objects.create(
                user=user,  # FK al usuario recién creado
                tipo_usuario='SECRETARIA',  # Automático para secretarias
                telefono=telefono,
                direccion=direccion,
                sexo=sexo if sexo in ['M', 'F', 'O'] else None,
                imagen_perfil_url=None  # No se pide imagen en este register
            )
            
            print(f"✅ PerfilUser creado: ID={perfil_user.id}, Tipo=SECRETARIA")
            
            # PASO 3: CREAR REGISTRO EN TABLA SECRETARIA
            # Importar aquí para evitar imports circulares
            from Administracion_Cond.models import Secretaria
            
            secretaria = Secretaria.objects.create(
                perfil=perfil_user,  # FK al perfil recién creado
                turno=turno,
                velocidad_teclado=velocidad_teclado
            )
            
            print(f"✅ Secretaria creada: ID={secretaria.perfil.id}, Turno={secretaria.turno}")
            
            # PASO 4: CREAR TOKEN PARA AUTENTICACIÓN
            token = Token.objects.create(user=user)
            
            return Response({
                "message": "Secretaria registration successful",
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
                },
                "secretaria": {
                    "id": secretaria.perfil.id,
                    "turno": secretaria.turno,
                    "velocidad_teclado": secretaria.velocidad_teclado
                }
            }, status=status.HTTP_201_CREATED)
            
    except Exception as e:
        print(f"❌ Error en registro de secretaria: {str(e)}")
        return Response({
            'error': 'Secretaria registration failed', 
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# =================================================================
# CREATE USER COMPLETE - Crear Usuario Completo (User + PerfilUser + Propietario/Guardia)
# =================================================================
@api_view(['POST'])
def CreateUserComplete(request):
    """
    Crear usuario completo: User + PerfilUser + (Propietario o Guardia)
    Solo permite crear PROPIETARIO y GUARDIA
    GUARDIA → is_staff=True (acceso administrativo)
    PROPIETARIO → is_staff=False (acceso normal)
    """
    try:
        with transaction.atomic():
            # DATOS PARA AUTH_USER
            username = request.data.get('username')
            email = request.data.get('email')
            password = request.data.get('password')
            first_name = request.data.get('first_name', '')
            last_name = request.data.get('last_name', '')
            
            # DATOS PARA PERFILUSER
            telefono = request.data.get('telefono', '')
            direccion = request.data.get('direccion', '')
            sexo = request.data.get('sexo', '')
            tipo_usuario = request.data.get('tipo_usuario')
            
            # VALIDACIONES BÁSICAS
            if not username or not email or not password:
                return Response({
                    'error': 'Username, email and password are required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if not tipo_usuario:
                return Response({
                    'error': 'tipo_usuario is required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # VALIDAR QUE SOLO SEA PROPIETARIO O GUARDIA
            if tipo_usuario not in ['PROPIETARIO', 'GUARDIA']:
                return Response({
                    'error': 'Only PROPIETARIO and GUARDIA types are allowed'
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
            
            # ✅ LÓGICA DE PERMISOS SEGÚN TIPO DE USUARIO
            is_staff = (tipo_usuario == 'GUARDIA')  # Solo GUARDIA tiene acceso staff
            is_superuser = False  # Nunca superuser para estos tipos
            
            # PASO 1: CREAR USUARIO EN AUTH_USER
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_superuser=is_superuser,
                is_staff=is_staff,  # ✅ True solo para GUARDIA
                is_active=True
            )
            
            print(f"✅ Usuario creado: ID={user.id}, Username={user.username}, is_staff={is_staff}")
            
            # PASO 2: CREAR PERFIL DE USUARIO
            perfil_user = PerfilUser.objects.create(
                user=user,
                tipo_usuario=tipo_usuario,
                telefono=telefono,
                direccion=direccion,
                sexo=sexo if sexo in ['M', 'F', 'O'] else None,
                imagen_perfil_url=None
            )
            
            print(f"✅ PerfilUser creado: ID={perfil_user.id}, Tipo={tipo_usuario}")
            
            # PASO 3: CREAR REGISTRO ESPECÍFICO SEGÚN TIPO
            specific_data = None
            
            if tipo_usuario == 'PROPIETARIO':
                # DATOS ESPECÍFICOS DE PROPIETARIO
                codigo_propietario = request.data.get('codigo_propietario')
                
                if not codigo_propietario:
                    return Response({
                        'error': 'codigo_propietario is required for PROPIETARIO'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # Verificar que el código no exista
                from Propietarios_Cond.models import Propietario
                if Propietario.objects.filter(codigo_propietario=codigo_propietario).exists():
                    return Response({
                        'error': 'codigo_propietario already exists'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # Crear Propietario
                propietario = Propietario.objects.create(
                    perfil=perfil_user,
                    codigo_propietario=codigo_propietario,
                    is_activo=True  # Siempre activo al crear
                )
                
                specific_data = {
                    "tipo": "propietario",
                    "id": propietario.perfil.id,
                    "codigo_propietario": propietario.codigo_propietario,
                    "is_activo": propietario.is_activo
                }
                print(f"✅ Propietario creado: Código={codigo_propietario}, is_staff={is_staff}")
                
            elif tipo_usuario == 'GUARDIA':
                # DATOS ESPECÍFICOS DE GUARDIA
                turno = request.data.get('turno', 'MAÑANA')
                fecha_contratacion = request.data.get('fecha_contratacion')
                informacion_adicional = request.data.get('informacion_adicional', '')
                
                # Validar turno
                if turno not in ['MAÑANA', 'TARDE', 'NOCHE']:
                    return Response({
                        'error': 'turno must be MAÑANA, TARDE, or NOCHE'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # Validar fecha de contratación
                if not fecha_contratacion:
                    return Response({
                        'error': 'fecha_contratacion is required for GUARDIA (format: YYYY-MM-DD)'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # Crear Guardia
                from Seguridad_Cond.models import Guardia
                from datetime import datetime
                
                try:
                    # Convertir fecha string a date object
                    fecha_obj = datetime.strptime(fecha_contratacion, '%Y-%m-%d').date()
                except ValueError:
                    return Response({
                        'error': 'fecha_contratacion must be in format YYYY-MM-DD'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                guardia = Guardia.objects.create(
                    perfil=perfil_user,
                    turno=turno,
                    is_activo=True,  # Siempre activo al crear
                    fecha_contratacion=fecha_obj,
                    informacion_adicional=informacion_adicional
                )
                
                specific_data = {
                    "tipo": "guardia",
                    "id": guardia.perfil.id,
                    "turno": guardia.turno,
                    "is_activo": guardia.is_activo,
                    "fecha_contratacion": guardia.fecha_contratacion,
                    "informacion_adicional": guardia.informacion_adicional
                }
                print(f"✅ Guardia creado: Turno={turno}, is_staff={is_staff}")
            
            # PASO 4: CREAR TOKEN
            token = Token.objects.create(user=user)
            
            return Response({
                "message": f"{tipo_usuario} created successfully",
                "token": token.key,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "is_superuser": user.is_superuser,
                    "is_staff": user.is_staff  # ✅ True para GUARDIA, False para PROPIETARIO
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
                "specific_data": specific_data,
                "permissions": {
                    "has_admin_access": user.is_staff,  # ✅ Indica si tiene acceso administrativo
                    "user_type": tipo_usuario
                }
            }, status=status.HTTP_201_CREATED)
            
    except Exception as e:
        print(f"❌ Error en creación de usuario completo: {str(e)}")
        return Response({
            'error': 'User creation failed', 
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# =================================================================
# REGISTER ADMINISTRADOR - Crear User + PerfilUser (sin tabla Administrador)
# =================================================================
@api_view(['POST'])
def RegisterAdministrador(request):
    """
    Registro específico para Administradores - Crea SOLO User y PerfilUser
    NO crea tabla Administrador porque no existe
    ADMINISTRADOR: is_staff=True, is_superuser=False, tipo_usuario="ADMINISTRADOR"
    """
    try:
        with transaction.atomic():
            # DATOS PARA AUTH_USER
            username = request.data.get('username')
            email = request.data.get('email')
            password = request.data.get('password')
            first_name = request.data.get('first_name', '')
            last_name = request.data.get('last_name', '')
            
            # DATOS PARA PERFILUSER
            telefono = request.data.get('telefono', '')
            direccion = request.data.get('direccion', '')
            sexo = request.data.get('sexo', '')
            
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
            
            # PASO 1: CREAR USUARIO EN AUTH_USER
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_superuser=False,  # Administrador NO es superuser
                is_staff=True,       # Administrador SÍ tiene acceso staff
                is_active=True
            )
            
            print(f"✅ Usuario creado: ID={user.id}, Username={user.username}, Tipo=ADMINISTRADOR")
            
            # PASO 2: CREAR PERFIL DE USUARIO (tipo_usuario = ADMINISTRADOR)
            perfil_user = PerfilUser.objects.create(
                user=user,  # FK al usuario recién creado
                tipo_usuario='ADMINISTRADOR',  # Automático para administradores
                telefono=telefono,
                direccion=direccion,
                sexo=sexo if sexo in ['M', 'F', 'O'] else None,
                imagen_perfil_url=None
            )
            
            print(f"✅ PerfilUser creado: ID={perfil_user.id}, Tipo=ADMINISTRADOR")
            
            # ❌ NO SE CREA TABLA ADMINISTRADOR PORQUE NO EXISTE
            # Solo se identifican por perfil_user.tipo_usuario = "ADMINISTRADOR"
            
            # PASO 3: CREAR TOKEN PARA AUTENTICACIÓN
            token = Token.objects.create(user=user)
            
            return Response({
                "message": "Administrador registration successful",
                "token": token.key,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "is_superuser": user.is_superuser,  # False
                    "is_staff": user.is_staff           # True
                },
                "perfil": {
                    "id": perfil_user.id,
                    "tipo_usuario": perfil_user.tipo_usuario,  # "ADMINISTRADOR"
                    "tipo_usuario_display": perfil_user.get_tipo_usuario_display(),  # "Administrador"
                    "telefono": perfil_user.telefono,
                    "direccion": perfil_user.direccion,
                    "sexo": perfil_user.sexo,
                    "imagen_perfil_url": perfil_user.imagen_perfil_url
                },
                "permissions": {
                    "is_staff": True,
                    "is_superuser": False,
                    "access_level": "ADMINISTRADOR",
                    "note": "Administrador identificado por perfil.tipo_usuario"
                }
            }, status=status.HTTP_201_CREATED)
            
    except Exception as e:
        print(f"❌ Error en registro de administrador: {str(e)}")
        return Response({
            'error': 'Administrador registration failed', 
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
