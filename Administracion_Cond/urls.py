from django.urls import path, include
from rest_framework import routers
from .api import SecretariaViewSet , PagoDespensaViewSet

router = routers.DefaultRouter()
router.register(r'secretarias', SecretariaViewSet, basename='secretarias')
router.register(r'pagos-despensa', PagoDespensaViewSet, basename='pagos_despensa')


urlpatterns = [
    path('', include(router.urls)),
]