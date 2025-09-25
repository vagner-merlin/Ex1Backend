from django.urls import path, include
from rest_framework import routers
from . import api

# Router para todos los ViewSets
router = routers.DefaultRouter()
router.register(r'guardias', api.GuardiaViewSet, basename='guardias')
router.register(r'secretarias', api.SecretariaViewSet, basename='secretarias')
router.register(r'administradores', api.AdministradorViewSet, basename='administradores')
router.register(r'propietarios', api.PropietarioViewSet, basename='propietarios')
router.register(r'areas-sociales', api.AreaSocialViewSet, basename='areas-sociales')
router.register(r'reservas-areas', api.ReservaAreaViewSet, basename='reservas-areas')
router.register(r'visitas', api.VisitaViewSet, basename='visitas')
router.register(r'quejas', api.QuejaViewSet, basename='quejas')
router.register(r'deudas', api.DeudaViewSet, basename='deudas')
# URLs de la app gestion
urlpatterns = [
    path('', include(router.urls)),
]