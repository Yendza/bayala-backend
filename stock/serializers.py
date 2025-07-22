from rest_framework import serializers
from .models import Stock
from produtos.models import Produto
from django.db import transaction

class ProdutoSimplesSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.SerializerMethodField()

    class Meta:
        model = Produto
        fields = ['id', 'nome', 'categoria_nome']

    def get_categoria_nome(self, obj):
        return obj.categoria.nome if obj.categoria else None

class StockSerializer(serializers.ModelSerializer):
    produto = ProdutoSimplesSerializer(read_only=True)
    produto_id = serializers.PrimaryKeyRelatedField(
        queryset=Produto.objects.all(),
        source='produto',
        write_only=True
    )

    class Meta:
        model = Stock
        fields = ['id', 'produto', 'produto_id', 'quantidade', 'data_entrada']

    def create(self, validated_data):
        with transaction.atomic():
        # Sempre cria nova linha no banco
            return Stock.objects.create(**validated_data)
