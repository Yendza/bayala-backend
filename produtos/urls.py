from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoriaViewSet,
    ProdutoViewSet,
    ProdutoListaAPIView,
)

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'produtos', ProdutoViewSet, basename='produtos')

urlpatterns = [
    path('', include(router.urls)),
    path('produtos-lista/', ProdutoListaAPIView.as_view(), name='produtos-lista'),
]
