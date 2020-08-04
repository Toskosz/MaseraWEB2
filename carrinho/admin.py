from django.contrib import admin
from .models import ItemCompra, Compra


class ListandoCompras(admin.ModelAdmin):
    list_display = ('codigo_de_referencia', 'comprador', 'finalizada', 'data_de_compra')
    search_fields = ('comprador__cpf', 'codigo_de_referencia',)
    filter_horizontal = ('itens',)


class ListandoItens(admin.ModelAdmin):
    list_display = ('cliente', 'produto', 'tamanho', 'quantidade', 'data_de_compra')
    search_fields = ('cliente__cpf',)


admin.site.register(ItemCompra, ListandoItens)

admin.site.register(Compra, ListandoCompras)
