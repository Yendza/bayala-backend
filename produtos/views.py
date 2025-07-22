from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view

from .models import Categoria, Produto
from .serializers import CategoriaSerializer, ProdutoSerializer

@api_view(['GET'])
def lista_categorias(request):
    categorias = Produto.objects.values_list('categoria', flat=True).distinct()
    return Response(list(categorias))

class CategoriaListView(APIView):
    def get(self, request):
        categorias = Categoria.objects.all()
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data)

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

# API com suporte a busca por nome para autocomplete
class ProdutoListaAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        search = request.query_params.get('search', '').strip().lower()
        produtos = Produto.objects.all()

        if search:
            produtos = produtos.filter(nome__icontains=search)

        data = [
            {
                "id": p.id,
                "nome": p.nome,
                "categoria_nome": p.categoria.nome if p.categoria else None,
                "preco_venda": str(p.preco_venda) if p.preco_venda is not None else None,
                "preco_aluguer": str(p.preco_aluguer) if p.preco_aluguer is not None else None,
                "activo": p.activo,
            }
            for p in produtos
        ]
        return Response(data)
