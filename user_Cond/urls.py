from django.urls import path, include
from rest_framework import routers
from .api import UserViewSet, GroupViewSet, PerfilUserViewSet
from . import views

# Router para ViewSets CRUD
router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'groups', GroupViewSet, basename='groups')
router.register(r'perfiles', PerfilUserViewSet, basename='perfiles')

# URLs combinadas
urlpatterns = [
    # CRUD endpoints
    path('', include(router.urls)),
    
    # Authentication endpoints
    path('auth/register/', views.Register, name='register'),
    path('auth/login/', views.Login, name='login'),
    path('auth/profile/', views.Profile, name='profile'),
    path('auth/logout/', views.Logout, name='logout'),
]
