from django.db import models
from transacao.form_choices import Estados
from transacao.form_choices import mes_choices
from transacao.form_choices import ano_choices


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
    mesValidadeCartao = models.CharField(max_length=5, choices=mes_choices, default=0)
    anoValidadeCartao = models.CharField(max_length=5, choices=ano_choices, default=0)
    segurancaCartao = models.CharField(max_length=10)

    def __str__(self):
        return self.transacao_id

