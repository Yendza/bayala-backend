from django.urls import path
from .views import (
    RelatorioVendasCompletoView,
    exportar_vendas_excel,
    exportar_vendas_pdf,
)

urlpatterns = [
    path('vendas-completo/', RelatorioVendasCompletoView.as_view(), name='relatorio-vendas-completo'),
    path('exportar/vendas_excel/', exportar_vendas_excel, name='exportar-vendas-excel'),
    path('exportar/vendas_pdf/', exportar_vendas_pdf, name='exportar-vendas-pdf'),
]
