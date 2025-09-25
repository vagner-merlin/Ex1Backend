from django.urls import path, include
from rest_framework import routers
from . import api

router = routers.DefaultRouter()
router.register(r'Propiedad', api.UnidadHabitacionalViewSet, basename='Propiedad')  # ← basename, no name

urlpatterns = [
    path('', include(router.urls)),
]