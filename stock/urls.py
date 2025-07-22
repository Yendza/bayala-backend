from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StockViewSet, stock_agrupado, lista_entradas_stock, stock_disponivel

router = DefaultRouter()
router.register('', StockViewSet, basename='stock')  # Endpoint: /api/stock/

urlpatterns = [
    path('stock-agrupado/', stock_agrupado, name='stock-agrupado'),
    path('entradas/', lista_entradas_stock, name='lista-entradas-stock'),
    path('stock-disponivel/', stock_disponivel, name='stock_disponivel'),
    path('', include(router.urls)),
]
