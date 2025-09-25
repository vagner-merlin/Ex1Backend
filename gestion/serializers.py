from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Guardia, Secretaria, Administrador, Propietario, AreaSocial, ReservaArea

# ------------------------------------------------------------------
# Serializador para el modelo Guardia
# ------------------------------------------------------------------
class GuardiaSerializer(serializers.ModelSerializer):
    # Campos del modelo User a los que accedemos a través de la relación OneToOne
    # ⚠️ ESTOS CAMPOS SON SOLO LECTURA - NO SE PUEDEN MODIFICAR DESDE AQUÍ
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    
    class Meta:
        model = Guardia
        fields = ['user', 'turno', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['user']  # El user no se puede cambiar una vez creado
        
    # ❌ NO PUEDES HACER:
    # - Cambiar el username, email, first_name, last_name desde este serializer
    # - Cambiar el user una vez creado el Guardia
    # ✅ SÍ PUEDES HACER:
    # - Crear: asignar un user existente y un turno
    # - Leer: ver todos los datos (incluyendo datos del User)
    # - Actualizar: solo el campo 'turno'
    # - Eliminar: borrar el registro completo

# ------------------------------------------------------------------
# Serializador para el modelo Secretaria
# ------------------------------------------------------------------
class SecretariaSerializer(serializers.ModelSerializer):
    # ⚠️ CAMPOS DE SOLO LECTURA DEL USER
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    
    class Meta:
        model = Secretaria
        fields = ['user', 'turno', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['user']
        
    # ❌ NO PUEDES: Modificar datos del User desde aquí
    # ✅ SÍ PUEDES: Solo modificar el campo 'turno'

# ------------------------------------------------------------------
# Serializador para el modelo Administrador
# ------------------------------------------------------------------
class AdministradorSerializer(serializers.ModelSerializer):
    # ⚠️ CAMPOS DE SOLO LECTURA DEL USER
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    
    class Meta:
        model = Administrador
        fields = ['user', 'cargo', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['user']
        
    # ❌ NO PUEDES: Modificar datos del User desde aquí
    # ✅ SÍ PUEDES: Solo modificar el campo 'cargo'

# ------------------------------------------------------------------
# Serializador para el modelo Propietario
# ------------------------------------------------------------------
class PropietarioSerializer(serializers.ModelSerializer):
    # ⚠️ CAMPOS DE SOLO LECTURA DEL USER Y CODIGO
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    
    class Meta:
        model = Propietario
        fields = ['user', 'codigo_propietario', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['codigo_propietario', 'user']
        
    # ❌ NO PUEDES: 
    # - Modificar datos del User desde aquí
    # - Cambiar el codigo_propietario (se genera automáticamente)
    # ✅ SÍ PUEDES: Solo leer todos los datos

# ------------------------------------------------------------------
# Serializador adicional para crear registros (opcional)
# ------------------------------------------------------------------
class GuardiaCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear nuevos guardias"""
    
    class Meta:
        model = Guardia
        fields = ['user', 'turno']
        
    def validate_user(self, value):
        """Valida que el user no tenga ya un perfil de guardia"""
        if Guardia.objects.filter(user=value).exists():
            raise serializers.ValidationError("Este usuario ya tiene un perfil de guardia")
        return value
    
    # ✅ ESTE SERIALIZER SÍ PERMITE: Crear guardias asignando users existentes


class AreaSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaSocial
        fields = '__all__'

class ReservaAreaSerializer(serializers.ModelSerializer):
    # Campos de solo lectura para mostrar información del propietario y área
    propietario_codigo = serializers.CharField(source='propietario.codigo_propietario', read_only=True)
    propietario_username = serializers.CharField(source='propietario.user.username', read_only=True)
    area_social_nombre = serializers.CharField(source='area_social.nombre', read_only=True)
    
    class Meta:
        model = ReservaArea
        fields = '__all__'