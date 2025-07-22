from django.urls import path
from . import views

urlpatterns = [
    path('utilizadores/', views.GerirUtilizadoresView.as_view(), name='gerir-utilizadores'),
    path('utilizadores/<int:pk>/', views.GerirUtilizadoresView.as_view(), name='gerir-utilizador-detail'),
    path('permissoes/', views.GerirPermissoesView.as_view(), name='gerir-permissoes'),
]
