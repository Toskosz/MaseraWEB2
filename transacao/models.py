from django.db import models
from transacao.estados import Estados


class Transacao(models.Model):
    transacao_id = models.CharField(max_length=15)
    endereco = models.CharField(max_length=200)
    complemento = models.CharField(max_length=200)
    cidade = models.CharField(max_length=150)
    bairro = models.CharField(max_length=150)
    pais = models.CharField(max_length=100)
    estado = models.CharField(max_length=3, choices=Estados.choices, default=0)
    cep = models.CharField(max_length=20)
    numeroCartao = models.CharField(max_length=50)
    nomeCartao = models.CharField(max_length=100)
    validadeCartao = models.CharField(max_length=10)
    segurancaCartao = models.CharField(max_length=10)

    def __str__(self):
        return self.transacao_id

