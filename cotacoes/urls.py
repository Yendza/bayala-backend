from rest_framework.routers import DefaultRouter
from .views import CotacaoViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'cotacoes', CotacaoViewSet, basename='cotacoes')

urlpatterns = [
    path('', include(router.urls)),
]
