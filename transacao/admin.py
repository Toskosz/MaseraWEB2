from django.contrib import admin
from .models import Transacao


class ListandoTransacoes(admin.ModelAdmin):
    search_fields = ('transacao_id',)
    list_per_page = 5


admin.site.register(Transacao, ListandoTransacoes)
