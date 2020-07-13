from django.contrib import admin
from .models import ItemCompra, Compra


class ListandoCompras(admin.ModelAdmin):
    list_display = ('comprador', 'finalizada', 'data_de_compra')
    search_fields = ('comprador__nome',)


class ListandoItens(admin.ModelAdmin):
    list_display = ('cliente', 'produto', 'tamanho', 'quantidade', 'data_de_compra')
    search_fields = ('cliente__nome',)


admin.site.register(ItemCompra, ListandoItens)

admin.site.register(Compra, ListandoCompras)
