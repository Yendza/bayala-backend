from django.urls import path
from .views import usuario_logado
from .views import AlterarSenhaView

urlpatterns = [
    path('usuario-logado/', usuario_logado, name='usuario-logado'),
    path('alterar-senha/', AlterarSenhaView.as_view(), name='alterar-senha'),
]
