from django import forms
from transacao.models import Transacao
from transacao.validations import *


class TransacaoForms(forms.ModelForm):
    complemento = forms.CharField(max_length=200, required=False)
    class Meta:
        model = Transacao
        exclude = ['transacao_id']
        labels = {'endereco': 'Endereço para entrega', 'complemento': 'Complemento', 'cidade': 'Cidade', 'bairro': 'Bairro',
                  'pais': 'País', 'estado': 'Estado', 'cep': 'CEP', 'numeroCartao': 'Número no cartão', 'nomeCartao': 'Nome no cartão',
                  'mesValidadeCartao': 'Mês vencimento', 'anoValidadeCartao': 'Ano vencimento',
                  'segurancaCartao': 'Código de segurança do cartão'}

    def clean(self):
        endereco = self.cleaned_data.get('endereco')
        complemento = self.cleaned_data.get('complemento')
        cidade = self.cleaned_data.get('cidade')
        bairro = self.cleaned_data.get('bairro')
        pais = self.cleaned_data.get('pais')
        estado = self.cleaned_data.get('estado')
        cep = self.cleaned_data.get('cep')
        numeroCartao = self.cleaned_data.get('numeroCartao')
        nomeCartao = self.cleaned_data.get('nomeCartao')
        mesValidadeCartao = self.cleaned_data.get('mesValidadeCartao')
        anoValidadeCartao = self.cleaned_data.get('anoValidadeCartao')
        segurancaCartao = self.cleaned_data.get('segurancaCartao')
        lista_de_erros = {}
        campo_vazio(endereco, 'endereco', lista_de_erros)
        if not campo_vazio(cidade, 'cidade', lista_de_erros):
            campo_tem_numero(cidade, 'cidade', lista_de_erros)
        campo_vazio(bairro, 'bairro', lista_de_erros)
        if not campo_vazio(pais, 'pais', lista_de_erros):
            campo_tem_numero(pais, 'pais', lista_de_erros)
        # if not campo_vazio(estado, 'estado', lista_de_erros):
        #     campo_tem_numero(estado, 'estado', lista_de_erros)
        if not campo_vazio(cep, 'cep', lista_de_erros):
            campo_tem_letra(cep, 'cep', lista_de_erros)
        if not campo_vazio(numeroCartao, 'numeroCartao', lista_de_erros):
            campo_tem_letra(numeroCartao, 'numeroCartao', lista_de_erros)
        if not campo_vazio(nomeCartao, 'nomeCartao', lista_de_erros):
            campo_tem_numero(nomeCartao, 'nomeCartao', lista_de_erros)
        # campo_vazio(validadeCartao, 'validadeCartao', lista_de_erros)
        # campo_tem_letra(validadeCartao, 'validadeCartao', lista_de_erros)
        if not campo_vazio(segurancaCartao, 'segurancaCartao', lista_de_erros):
            campo_tem_letra(segurancaCartao, 'segurancaCartao', lista_de_erros)
        if lista_de_erros is not None:
            for erro in lista_de_erros:
                mensagem_erro = lista_de_erros[erro]
                self.add_error(erro, mensagem_erro)
        return self.cleaned_data
