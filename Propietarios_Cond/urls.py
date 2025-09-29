from django.urls import path, include
from rest_framework import routers
from .api import *

router = routers.DefaultRouter()
router.register(r'propietarios', PropietarioViewSet, basename='propietarios')
router.register(r'quejas', QuejaViewSet, basename='quejas')
router.register(r'movilidad', MobilitadViewSet, basename='movilidad')
router.register(r'unidades-habitacionales', UnidadHabitacionalViewSet, basename='unidades_habitacionales')
router.register(r'propietarios-unidades', PropietarioUnidadViewSet, basename='propietarios_unidades')
router.register(r'areas-sociales', AreaSocialViewSet, basename='areas_sociales')
router.register(r'registros-areas-sociales', RegistroAreaSocialViewSet, basename='registros_areas_sociales')

urlpatterns = [
    path('', include(router.urls)),
]