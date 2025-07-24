from django.core.management.base import BaseCommand
from stock.models import Stock

class Command(BaseCommand):
    help = 'Limpa registros duplicados de stock, somando quantidades iguais'

    def handle(self, *args, **kwargs):
        for produto_id in Stock.objects.values_list('produto_id', flat=True).distinct():
            stocks = Stock.objects.filter(produto_id=produto_id)
            if stocks.count() > 1:
                total = sum(s.quantidade for s in stocks)
                stock = stocks.first()
                stock.quantidade = total
                stock.save()
                stocks.exclude(id=stock.id).delete()

        self.stdout.write(self.style.SUCCESS("Limpeza de stock concluída."))
