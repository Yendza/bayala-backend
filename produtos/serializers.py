from rest_framework import serializers
from .models import Categoria, Produto
from stock.models import Stock

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nome']

class ProdutoSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.SerializerMethodField()
    categoria_id = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(),
        source='categoria',
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = Produto
        fields = [
            'id',
            'nome',
            'descricao',
            'preco_venda',
            'preco_aluguer',
            'categoria_id',
            'categoria_nome',
            'activo',
        ]

    def get_quantidade(self, obj):
        stock = Stock.objects.filter(produto=obj).first()
        return stock.quantidade if stock else 0

    def get_categoria_nome(self, obj):
        return obj.categoria.nome if obj.categoria else None


