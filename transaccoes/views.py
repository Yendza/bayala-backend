from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.dateparse import parse_date
from .models import Produto, Cliente, Transaccao, ItemTransaccao
from stock.models import Stock  # IMPORTAÇÃO CORRETA
from .serializers import ProdutoSerializer, ClienteSerializer, TransaccaoSerializer, ItemTransaccaoSerializer
from django.db.models import Sum


# --------------------------
# CRUD ViewSets protegidos
# --------------------------
class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    permission_classes = [IsAuthenticated]


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]


class TransaccaoViewSet(viewsets.ModelViewSet):
    queryset = Transaccao.objects.all().order_by('-data')
    serializer_class = TransaccaoSerializer
    permission_classes = [IsAuthenticated]


class ItemTransaccaoViewSet(viewsets.ModelViewSet):
    queryset = ItemTransaccao.objects.all()
    serializer_class = ItemTransaccaoSerializer
    permission_classes = [IsAuthenticated]


# --------------------------
# Dashboard Resumido com Alertas Stock
# --------------------------

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    total_transaccoes = Transaccao.objects.count()
    total_produtos = Produto.objects.count()
    total_clientes = Cliente.objects.count()

    # Receita total
    total_receita = 0
    for item in ItemTransaccao.objects.select_related('produto'):
        preco_unit = item.produto.preco_venda if item.tipo == 'venda' else item.produto.preco_aluguer
        total_receita += preco_unit * item.quantidade

    # Stock agrupado (quantidade total por produto)
    limite_critico = 5
    stock_agrupado = (
        Stock.objects
        .values('produto__id', 'produto__nome')
        .annotate(quantidade_total=Sum('quantidade'))
        .filter(quantidade_total__lte=limite_critico)
    )

    alertas = [
        {
            'produto_id': item['produto__id'],
            'nome': item['produto__nome'],
            'quantidade_disponivel': item['quantidade_total'],
            'mensagem': f'Stock baixo: {item["quantidade_total"]} unidades restantes'
        }
        for item in stock_agrupado
    ]

    return Response({
        'transaccoes': total_transaccoes,
        'produtos': total_produtos,
        'clientes': total_clientes,
        'receita': total_receita,
        'alertas_stock': alertas,
    })



# --------------------------
# Relatório Completo de Vendas
# --------------------------
class RelatorioVendasCompletoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        start_date = request.query_params.get('start_date') or request.query_params.get('data_inicio')
        end_date = request.query_params.get('end_date') or request.query_params.get('data_fim')
        cliente_id = request.query_params.get('cliente_id') or request.query_params.get('cliente')
        produto_id = request.query_params.get('produto_id')
        tipo_pagamento = request.query_params.get('tipo_pagamento')
        tipo_transacao = request.query_params.get('tipo_transacao')

        transacoes = Transaccao.objects.all()

        if start_date:
            transacoes = transacoes.filter(data__date__gte=parse_date(start_date))
        if end_date:
            transacoes = transacoes.filter(data__date__lte=parse_date(end_date))
        if cliente_id:
            transacoes = transacoes.filter(cliente_id=cliente_id)
        if tipo_pagamento:
            transacoes = transacoes.filter(tipo_pagamento=tipo_pagamento)
        if tipo_transacao:
            transacoes = transacoes.filter(tipo=tipo_transacao)

        total_receita = 0
        total_produtos = 0
        vendas_por_produto = {}
        vendas_por_cliente = {}
        vendas_por_tipo_pagamento = {}
        ultimas_transacoes = []

        for t in transacoes:
            trans_total = 0
            for item in t.itens.all():
                preco_unit = item.produto.preco_venda if item.tipo == 'venda' else item.produto.preco_aluguer
                subtotal = preco_unit * item.quantidade
                trans_total += subtotal
                total_produtos += item.quantidade

                pid = item.produto.id
                if pid not in vendas_por_produto:
                    vendas_por_produto[pid] = {
                        'produto__id': pid,
                        'produto__nome': item.produto.nome,
                        'quantidade_vendida': 0,
                        'receita': 0,
                    }
                vendas_por_produto[pid]['quantidade_vendida'] += item.quantidade
                vendas_por_produto[pid]['receita'] += subtotal

            cid = t.cliente.id
            if cid not in vendas_por_cliente:
                vendas_por_cliente[cid] = {
                    'cliente__id': cid,
                    'cliente__nome': t.cliente.nome,
                    'total_vendas': 0,
                    'num_transacoes': 0
                }
            vendas_por_cliente[cid]['total_vendas'] += trans_total
            vendas_por_cliente[cid]['num_transacoes'] += 1

            tipo = t.tipo_pagamento
            if tipo not in vendas_por_tipo_pagamento:
                vendas_por_tipo_pagamento[tipo] = {
                    'tipo_pagamento': tipo,
                    'total': 0,
                    'num_transacoes': 0
                }
            vendas_por_tipo_pagamento[tipo]['total'] += trans_total
            vendas_por_tipo_pagamento[tipo]['num_transacoes'] += 1

            total_receita += trans_total

            ultimas_transacoes.append({
                'id': t.id,
                'data': t.data,
                'cliente__nome': t.cliente.nome,
                'tipo_pagamento': t.tipo_pagamento,
            })

        return Response({
            'total_receita': total_receita,
            'total_transacoes': transacoes.count(),
            'total_produtos_vendidos': total_produtos,
            'vendas_por_produto': list(vendas_por_produto.values()),
            'vendas_por_cliente': list(vendas_por_cliente.values()),
            'vendas_por_tipo_pagamento': list(vendas_por_tipo_pagamento.values()),
            'ultimas_transacoes': sorted(ultimas_transacoes, key=lambda x: x['data'], reverse=True)[:10]
        })
