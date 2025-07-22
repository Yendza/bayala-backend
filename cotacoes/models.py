from django.db import models
from produtos.models import Produto
from datetime import datetime

class Cotacao(models.Model):
    numero = models.CharField(max_length=20, unique=True, null=True, blank=True)
    nome_cliente = models.CharField(max_length=100)
    nuit_cliente = models.CharField(max_length=20, blank=True, null=True)
    celular_cliente = models.CharField(max_length=20, blank=True, null=True)
    data = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.numero:
            ano = datetime.now().year
            ultimo = Cotacao.objects.filter(data__year=ano).count() + 1
            self.numero = f"{str(ultimo).zfill(3)}/{ano}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Cotação {self.numero} - {self.nome_cliente}"

class ItemCotacao(models.Model):
    cotacao = models.ForeignKey(Cotacao, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    tipo = models.CharField(max_length=10, choices=[('venda', 'Venda'), ('aluguer', 'Aluguer')], default='venda')

    def __str__(self):
        return f"{self.produto.nome} ({self.tipo}) x{self.quantidade}"
