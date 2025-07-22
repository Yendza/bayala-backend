from rest_framework import serializers
from .models import Cotacao, ItemCotacao
from produtos.models import Produto
from decimal import Decimal
from stock.models import Stock  # ajusta conforme teu caminho real


class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ['id', 'nome', 'preco_venda', 'preco_aluguer']

class ItemCotacaoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCotacao
        fields = ['produto', 'quantidade', 'tipo']

class ItemCotacaoSerializer(serializers.ModelSerializer):
    produto = ProdutoSerializer(read_only=True)

    class Meta:
        model = ItemCotacao
        fields = ['id', 'produto', 'quantidade', 'tipo']

class CotacaoSerializer(serializers.ModelSerializer):
    itens = ItemCotacaoCreateSerializer(many=True, write_only=True)
    itens_detalhados = ItemCotacaoSerializer(many=True, read_only=True, source='itens')
    total = serializers.SerializerMethodField()
    data_formatada = serializers.SerializerMethodField()
    numero = serializers.ReadOnlyField()

    class Meta:
        model = Cotacao
        fields = [
            'id', 'numero', 'nome_cliente', 'nuit_cliente', 'celular_cliente',
            'data', 'data_formatada', 'itens', 'itens_detalhados', 'total'
        ]

    def get_total(self, obj):
        total = 0
        for item in obj.itens.all():
            preco = item.produto.preco_venda if item.tipo == 'venda' else item.produto.preco_aluguer
            total += item.quantidade * preco
        total_com_iva = total * Decimal('1.16')
        return f"{total_com_iva:.2f}"

    def get_data_formatada(self, obj):
        return obj.data.strftime('%d/%m/%Y %H:%M')

    
    def create(self, validated_data):
        itens_data = validated_data.pop('itens')
        erros_stock = []

        for item in itens_data:
            produto_id = item['produto'].id if isinstance(item['produto'], Produto) else item['produto']
            try:
                produto = Produto.objects.get(pk=produto_id)
            except Produto.DoesNotExist:
                raise serializers.ValidationError({
                    "produto": f"Produto com ID {produto_id} não encontrado."
                })

            quantidade_requerida = item['quantidade']

            # Verifica stock sem reduzir            
            estoque = Stock.objects.filter(produto=produto).first()
            if not estoque or estoque.quantidade < quantidade_requerida:
                erros_stock.append(
                    f"{produto.nome}: disponível {estoque.quantidade if estoque else 0}, solicitado {quantidade_requerida}"
                )

        if erros_stock:
            raise serializers.ValidationError({
                "stock": f"Stock insuficiente para os seguintes produtos:\n" + "\n".join(erros_stock)
            })

        cotacao = Cotacao.objects.create(**validated_data)

        for item in itens_data:
            produto_id = item['produto'].id if isinstance(item['produto'], Produto) else item['produto']
            produto = Produto.objects.get(pk=produto_id)

            ItemCotacao.objects.create(
                cotacao=cotacao,
                produto=produto,
                quantidade=item['quantidade'],
                tipo=item['tipo']
            )

        return cotacao
