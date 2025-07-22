from rest_framework import serializers
from decimal import Decimal
from .models import Transaccao, ItemTransaccao, Cliente
from produtos.models import Produto
from django.db.models import Sum
from django.db import transaction
from rest_framework.exceptions import ValidationError
from stock.models import Stock

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ['id', 'nome', 'preco_venda', 'preco_aluguer']

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nome', 'nuit', 'celular']

class ItemTransaccaoCreateSerializer(serializers.ModelSerializer):
    produto = serializers.PrimaryKeyRelatedField(queryset=Produto.objects.all())

    class Meta:
        model = ItemTransaccao
        fields = ['produto', 'quantidade', 'tipo']

class ItemTransaccaoSerializer(serializers.ModelSerializer):
    produto = ProdutoSerializer(read_only=True)

    class Meta:
        model = ItemTransaccao
        fields = ['id', 'produto', 'quantidade', 'tipo']

class TransaccaoSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer()
    itens = ItemTransaccaoCreateSerializer(many=True, write_only=True)
    itens_detalhados = ItemTransaccaoSerializer(many=True, read_only=True, source='itens')
    tipo_pagamento = serializers.ChoiceField(choices=Transaccao.TIPO_PAGAMENTO_CHOICES)
    total = serializers.SerializerMethodField()
    data_formatada = serializers.SerializerMethodField()
    numero = serializers.ReadOnlyField()

    class Meta:
        model = Transaccao
        fields = [
            'id', 'numero', 'cliente', 'data', 'data_formatada',
            'itens', 'itens_detalhados', 'tipo_pagamento', 'total'
        ]

    def get_total(self, obj):
        total = 0
        for item in obj.itens.all():
            preco = item.produto.preco_venda if item.tipo == 'venda' else item.produto.preco_aluguer
            total += item.quantidade * preco
        total_com_iva = total * Decimal('1.16')  # 16% IVA
        return f"{total_com_iva:.2f}"

    def get_data_formatada(self, obj):
        return obj.data.strftime('%d/%m/%Y %H:%M')

    def create(self, validated_data):
        cliente_data = validated_data.pop('cliente')
        itens_data = validated_data.pop('itens')

        # Criar ou obter cliente
        nuit = cliente_data.get('nuit')
        if nuit:
            cliente_obj, _ = Cliente.objects.get_or_create(
                nuit=nuit,
                defaults={
                    'nome': cliente_data.get('nome', ''),
                    'celular': cliente_data.get('celular', '')
                }
            )
        else:
            cliente_obj = Cliente.objects.create(
                nome=cliente_data.get('nome', ''),
                nuit=None,
                celular=cliente_data.get('celular', '')
            )

        erros_stock = []

        # Validação de stock: filtra só entradas com quantidade positiva
        for item in itens_data:
            produto_obj = item['produto'] if isinstance(item['produto'], Produto) else Produto.objects.get(pk=item['produto'])
            quantidade_requerida = item['quantidade']

            stock_total = Stock.objects.filter(produto=produto_obj, quantidade__gt=0).aggregate(
                total_quantidade=Sum('quantidade')
            )['total_quantidade'] or 0

            if stock_total < quantidade_requerida:
                erros_stock.append(
                    f"{produto_obj.nome}: disponível {stock_total}, solicitado {quantidade_requerida}"
                )

        if erros_stock:
            raise ValidationError({"stock": "Stock insuficiente:\n" + "\n".join(erros_stock)})

        with transaction.atomic():
            transaccao = Transaccao.objects.create(cliente=cliente_obj, **validated_data)

            for item in itens_data:
                produto_obj = item['produto'] if isinstance(item['produto'], Produto) else Produto.objects.get(pk=item['produto'])

                ItemTransaccao.objects.create(
                    transaccao=transaccao,
                    produto=produto_obj,
                    quantidade=item['quantidade'],
                    tipo=item['tipo']
                )

                # Deduz stock FIFO
                quantidade_a_deduzir = item['quantidade']
                entradas_stock = Stock.objects.filter(produto=produto_obj, quantidade__gt=0).order_by('data_entrada')

                for entrada in entradas_stock:
                    if quantidade_a_deduzir <= 0:
                        break

                    if entrada.quantidade <= quantidade_a_deduzir:
                        quantidade_a_deduzir -= entrada.quantidade
                        entrada.quantidade = 0
                    else:
                        entrada.quantidade -= quantidade_a_deduzir
                        quantidade_a_deduzir = 0

                    entrada.save()

        return transaccao
