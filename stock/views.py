from rest_framework import viewsets, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Stock
from .serializers import StockSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from produtos.models import Produto


class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.select_related('produto__categoria').order_by('-data_entrada')
    serializer_class = StockSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['produto__nome']


@api_view(['GET'])
def stock_agrupado(request):
    stock = Stock.objects.select_related('produto', 'produto__categoria').all()
    dados = {}

    for item in stock:
        produto = item.produto
        chave = f"{produto.id}"

        if chave not in dados:
            dados[chave] = {
                "produto": {
                    "id": produto.id,
                    "nome": produto.nome,
                    "categoria_nome": produto.categoria.nome if produto.categoria else "",
                },
                "quantidade": item.quantidade,
                "data_entrada": item.data_entrada,
            }
        else:
            dados[chave]["quantidade"] += item.quantidade
            if item.data_entrada > dados[chave]["data_entrada"]:
                dados[chave]["data_entrada"] = item.data_entrada

    return Response(list(dados.values()))


@api_view(['GET'])
def lista_entradas_stock(request):
    entradas = Stock.objects.select_related('produto', 'produto__categoria').order_by('data_entrada')
    resultado = []

    totais_por_produto = {}

    for entrada in entradas:
        produto = entrada.produto
        produto_id = produto.id

        quantidade_anterior = totais_por_produto.get(produto_id, 0)
        quantidade_adicionada = entrada.quantidade
        quantidade_actual = quantidade_anterior + quantidade_adicionada

        # Atualiza total acumulado para o produto
        totais_por_produto[produto_id] = quantidade_actual

        resultado.append({
            "id": entrada.id,
            "produto": {
                "id": produto.id,
                "nome": produto.nome,
                "categoria": produto.categoria.nome if produto.categoria else "",
            },
            "quantidade_anterior": quantidade_anterior,
            "quantidade_adicionada": quantidade_adicionada,
            "quantidade_actual": quantidade_actual,
            "data_entrada": entrada.data_entrada,
        })

    return Response(resultado)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def stock_disponivel(request):
    produto_id = request.query_params.get('produto_id')
    if not produto_id:
        return Response({"error": "produto_id é obrigatório"}, status=400)

    try:
        produto = Produto.objects.get(id=produto_id)
    except Produto.DoesNotExist:
        return Response({"error": "Produto não encontrado"}, status=404)

    total_stock = Stock.objects.filter(produto=produto, quantidade__gt=0).aggregate(
        total_quantidade=Sum('quantidade')
    )['total_quantidade'] or 0

    return Response({
        "produto_id": produto_id,
        "quantidade_disponivel": total_stock
    })