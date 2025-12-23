from django.db import models

class Empresa(models.Model):
    nome = models.CharField(max_length=200)
    endereco = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    telefone = models.CharField(max_length=50, blank=True, null=True)
    cnpj = models.CharField(max_length=20, blank=True, null=True)  # ou NIF
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome
