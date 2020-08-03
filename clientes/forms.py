from django import forms
from clientes.models import Cliente
from clientes.validations import *
from transacao.validations import *


class ClienteForms(forms.ModelForm):
    class Meta:
        model = Cliente
        exclude = ['user']
        labels = {'nome':'Nome', 'sobrenome':'Sobrenome', 'email':'Email para contato', 'cpf':'CPF',
                  'telefone':'Telefone para contato'}

    def clean(self):
        nome = self.cleaned_data.get('nome')
        sobrenome = self.cleaned_data.get('sobrenome')
        email = self.cleaned_data.get('email')
        cpf = self.cleaned_data.get('cpf')
        telefone = self.cleaned_data.get('telefone')
        lista_de_erros = {}
        if not campo_vazio(nome, 'nome', lista_de_erros):
            campo_tem_numero(nome, 'nome', lista_de_erros)
        if not campo_vazio(sobrenome, 'sobrenome', lista_de_erros):
            campo_tem_numero(sobrenome, 'sobrenome', lista_de_erros)
        email_invalido(email, 'email', lista_de_erros)
        if not campo_vazio(cpf, 'cpf', lista_de_erros):
            # campo_tem_letra(cpf, 'cpf', lista_de_erros)
            valida_cpf(cpf, 'cpf', lista_de_erros)
        if not campo_vazio(telefone, 'telefone', lista_de_erros):
            campo_tem_letra(telefone, 'telefone', lista_de_erros)
        if lista_de_erros is not None:
            for erro in lista_de_erros:
                mensagem_erro = lista_de_erros[erro]
                self.add_error(erro, mensagem_erro)
        return self.cleaned_data

