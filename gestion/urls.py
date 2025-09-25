from django.urls import path, include
from rest_framework import routers
from . import api

# Router para todos los ViewSets
router = routers.DefaultRouter()
router.register(r'guardias', api.GuardiaViewSet, basename='guardias')
router.register(r'secretarias', api.SecretariaViewSet, basename='secretarias')
router.register(r'administradores', api.AdministradorViewSet, basename='administradores')
router.register(r'propietarios', api.PropietarioViewSet, basename='propietarios')

# URLs de la app gestion
urlpatterns = [
    path('', include(router.urls)),
]