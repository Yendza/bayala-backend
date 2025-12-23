from django.contrib import admin
from .models import Empresa

admin.site.site_header = "Administração da CONTROLLER"
admin.site.site_title = "Administração da CONTROLLER"
admin.site.index_title = "Painel de Gestão"

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ("nome", "nuit", "telefone", "email")
    search_fields = ("nome", "nuit")


