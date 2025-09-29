from django.urls import path ,  include
from .api import GuardiaViewSet, VisitaViewSet 
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'guardias', GuardiaViewSet , basename='guardias')
router.register(r'visitas', VisitaViewSet , basename='visitas')

urlpatterns = [
    path('', include(router.urls)),
]