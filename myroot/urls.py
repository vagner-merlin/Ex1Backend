
from django.contrib import admin
from django.urls import path  , include
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('usuarios.urls')),
    path('api/', include('gestion.urls')),
    path('api/', include('Propiedad.urls')),
]
