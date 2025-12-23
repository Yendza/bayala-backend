from django.db import models
from core.models import Empresa  # importa o modelo Empresa

class Cliente(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="clientes")
    nome = models.CharField(max_length=255)
    nuit = models.CharField(max_length=50, blank=True, null=True)
    celular = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nome
