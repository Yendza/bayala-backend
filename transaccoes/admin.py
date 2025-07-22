from django.contrib import admin
from .models import Transaccao, ItemTransaccao, Cliente

admin.site.register(Transaccao)
admin.site.register(ItemTransaccao)
admin.site.register(Cliente)
