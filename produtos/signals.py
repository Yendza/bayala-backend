# produtos/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Produto
from stock.models import Stock

@receiver(post_save, sender=Produto)
def criar_stock_automatico(sender, instance, created, **kwargs):
    if created:
        Stock.objects.create(produto=instance)
