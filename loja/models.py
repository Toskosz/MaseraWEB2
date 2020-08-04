from django.db import models
from datetime import datetime

class Produto(models.Model):
    nome_produto = models.CharField(max_length=200)
    nome_url = models.CharField(max_length=200)
    descricao = models.TextField()
    categoria = models.CharField(max_length=100)
    date_produto = models.DateTimeField(default=datetime.now, blank=True)
    publicado = models.BooleanField(default=False)
    foto_produto = models.ImageField(upload_to='fotos/%Y/%m/%d/', blank=True)
    preco = models.IntegerField()
    disponibilidade = models.BooleanField(default=True)
    tamanho_pequeno = models.IntegerField()
    tamanho_medio = models.IntegerField()
    tamanho_grande = models.IntegerField()

    def __str__(self):
        return self.nome_produto
