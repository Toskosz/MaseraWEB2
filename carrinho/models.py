from django.db import models
from django.contrib.auth.models import User
from clientes.models import Cliente
from loja.models import Produto


class ItemCompra(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
    produto = models.ForeignKey(Produto, on_delete=models.SET_NULL, null=True)
    data_de_adicionamento = models.DateTimeField(auto_now=True)
    data_de_compra = models.DateTimeField(null=True)
    tamanho = models.CharField(max_length=2, default='x')
    quantidade = models.IntegerField(default=0)

    def __str__(self):
        return self.produto.nome_produto


class Compra(models.Model):
    codigo_de_referencia = models.CharField(max_length=15)
    comprador = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
    finalizada = models.BooleanField(default=False)
    itens = models.ManyToManyField(ItemCompra)
    data_de_compra = models.DateTimeField(auto_now=True)

    def get_itens_carrinho(self):
        return self.itens.all()

    def get_total_carrinho(self):
        total = 0
        for item in self.itens.all():
            total += item.produto.preco * item.quantidade
        return total

    def __str__(self):
        return '{} - {}'.format(self.comprador, self.codigo_de_referencia)