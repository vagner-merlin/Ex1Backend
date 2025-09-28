
from django.urls import path , include
from rest_framework import routers
from .api import UserViewSet , GroupViewSet , PerfilUserViewSet
 
#crea la rutas 
router = routers.DefaultRouter()
router.register(r'users', UserViewSet , basename='users')
router.register(r'groups', GroupViewSet , basename='groups')
router.register(r'perfiles', PerfilUserViewSet, basename='perfiles')

urlpatterns = [
   path('', include(router.urls)),
]
