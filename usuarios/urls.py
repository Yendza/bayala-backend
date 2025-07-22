# No arquivo: usuarios/urls.py
from django.urls import path
from .views import CustomTokenObtainPairView, usuario_logado, AlterarSenhaView

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('usuario-logado/', usuario_logado, name='usuario_logado'),
    path('alterar-senha/', AlterarSenhaView.as_view(), name='alterar_senha'),
]
