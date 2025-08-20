from django.db import models
from produtos.models import Produto
from datetime import datetime

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    nuit = models.CharField(max_length=20, blank=True, null=True)
    celular = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.nome} - {self.nuit or 'Sem NUIT'}"

class Transaccao(models.Model):
    numero = models.CharField(max_length=20, unique=True, null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)

    TIPO_PAGAMENTO_CHOICES = [
        ('mpesa', 'M-Pesa'),
        ('emola', 'E-Mola'),
        ('cheque', 'Cheque'),
        ('numerario', 'Numerário'),
        ('transferencia', 'Transferência Bancária'),
    ]
    tipo_pagamento = models.CharField(
        max_length=20,
        choices=TIPO_PAGAMENTO_CHOICES,
        default='numerario',
        blank=False,
        null=False,
        help_text="Tipo de pagamento usado na transacção"
    )

    def save(self, *args, **kwargs):
        if not self.numero:
            ano = datetime.now().year
            ultimo = Transaccao.objects.filter(data__year=ano).count() + 1
            self.numero = f"{str(ultimo).zfill(3)}/{ano}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Factura {self.numero} - {self.cliente.nome}"

class ItemTransaccao(models.Model):
    transaccao = models.ForeignKey(Transaccao, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    tipo = models.CharField(max_length=10, choices=[('venda', 'Venda'), ('aluguer', 'Aluguer')], default='venda')

    def __str__(self):
        return f"{self.produto.nome} ({self.tipo}) x{self.quantidade}"
