from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome da Categoria")

    def __str__(self):
        return self.nome

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    preco_aluguer = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    pode_ser_vendido = models.BooleanField(default=True)
    pode_ser_alugado = models.BooleanField(default=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


