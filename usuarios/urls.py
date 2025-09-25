
from django.urls import path, include
from rest_framework import routers
from . import api

# Router para el ViewSet (CRUD)
router = routers.DefaultRouter()
router.register(r'users', api.UserViewSet, basename='users')

# URLs de la app usuarios
urlpatterns = [
    # APIs de autenticación
    path('auth/login/', api.Login, name='login'),
    path('auth/register/', api.Register, name='register'),
    path('auth/profile/', api.Profile, name='profile'),
    
    # APIs del CRUD (ViewSet)
    path('', include(router.urls)),
]
 