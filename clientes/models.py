from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=255)
    nuit = models.CharField(max_length=50, blank=True, null=True)
    celular = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nome