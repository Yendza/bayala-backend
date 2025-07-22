from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    # Apps principais
    path('api/', include('produtos.urls')),
    path('api/', include('clientes.urls')),
    path('api/', include('transaccoes.urls')),
    path('api/', include('cotacoes.urls')),
    path('api/', include('usuarios.urls')),

    

    # Novas apps
    path('api/stock/', include('stock.urls')),
    path('api/relatorios/', include('relatorios.urls')),
    path('api/configuracoes/', include('configuracoes.urls')),

    # Autenticação JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
