from django.contrib import admin
from .models import Produto


class ListandoProdutos(admin.ModelAdmin):
    list_display = ('id', 'nome_produto', 'categoria', 'disponibilidade', 'publicado')
    list_display_links = ('id', 'nome_produto')
    search_fields = ('nome_produto',)
    list_filter = ('categoria',)
    list_per_page = 5
    list_editable = ('publicado',)


admin.site.register(Produto, ListandoProdutos)

