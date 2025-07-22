from django.contrib import admin
from .models import Categoria, Produto
from stock.models import Stock  # Corrigido: importar Stock da app correta


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)


class StockInline(admin.StackedInline):
    model = Stock
    extra = 0


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'preco_venda', 'preco_aluguer', 'activo')
    search_fields = ('nome',)
    list_filter = ('categoria', 'activo')
    inlines = [StockInline]