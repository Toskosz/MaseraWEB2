from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from carrinho.views import atual_compra_pendente
from django.contrib import messages, auth
from django.shortcuts import render, redirect, get_object_or_404
from clientes.models import Cliente
from clientes.forms import ClienteForms
from clientes.views import relog
from transacao.forms import TransacaoForms
from loja.models import Produto
from transacao.extras import gera_id_transacao
from .models import Transacao
import datetime
from datetime import datetime


@login_required()
def checkout(request, **kwargs):
    compra = atual_compra_pendente(request)
    itens = list(compra.get_itens_carrinho())
    total = compra.total
    cliente_form = ClienteForms()
    transacao_form = TransacaoForms()
    dados = {
        'order': itens,
        'total': total,
        'transacao_form': transacao_form,
        'cliente_form': cliente_form
    }
    return render(request, 'carrinho/checkout.html', dados)


@login_required()
def feedback(request, **kwargs):
    auth.logout(request)
    return render(request, 'carrinho/feedback.html')


@login_required()
def cofirma_compra(request):
    if request.method == 'POST':
        cliente_form = ClienteForms(request.POST)
        transacao_form = TransacaoForms(request.POST)
        if cliente_form.is_valid() and transacao_form.is_valid():
            compra_atual = atual_compra_pendente(request)
            itens_comprados = compra_atual.get_itens_carrinho()

            if verifica_estoque(request, list(itens_comprados)):
                return redirect('resumo_carrinho')
            else:
                cliente_temp = get_object_or_404(Cliente, user=request.user)
                cliente_final = Cliente.objects.filter(cpf=cliente_form.cleaned_data.get('cpf')).first()
                if cliente_final:
                    compra_atual.comprador = cliente_final
                    itens_comprados.update(cliente=cliente_final)
                    usuario_anterior = request.user
                    request.user = cliente_final.user
                    relog(request)
                    usuario_anterior.delete()
                    cliente_temp.delete()
                else:
                    cliente_temp.nome = cliente_form.cleaned_data.get('nome')
                    cliente_temp.sobrenome = cliente_form.cleaned_data.get('sobrenome')
                    cliente_temp.email = cliente_form.cleaned_data.get('email')
                    cliente_temp.telefone = cliente_form.cleaned_data.get('telefone')
                    cliente_temp.cpf = cliente_form.cleaned_data.get('cpf')
                    request.user.username = cliente_form.cleaned_data.get('cpf')
                    request.user.save()
                    cliente_temp.save()

                transacao = instancia_transacao(transacao_form)
                compra_atual.transacao = transacao
                compra_atual.save()
                return redirect('finaliza_compra')
        else:
            compra = atual_compra_pendente(request)
            itens = list(compra.get_itens_carrinho())
            total = compra.total
            dados = {
                'order': itens,
                'total': total,
                'transacao_form': transacao_form,
                'cliente_form': cliente_form
            }
            return render(request, 'carrinho/checkout.html', dados)


@login_required()
def finaliza_compra(request):
    compra_atual = atual_compra_pendente(request)
    itens_comprados = compra_atual.get_itens_carrinho()

    # transacao_arpovada é a função que vai utilizar a API de pagamento
    # if transacao_aprovada():
    #     ajusta_estoque(list(itens_comprados))
    #     itens_comprados.update(data_de_compra=datetime.now())
    #     compra_atual.finalizada = True
    #     compra_atual.data_de_compra = datetime.now()
    #     # API DE EMAIL
    #     return redirect('feedback')
    # else:
    #     compra_atual.transacao.delete()
    #     compra_atual.save()
    #     messages.error("Sua transação foi recusada, verifique seus dados de pagamento ou fale com seu banco.")
    #     return redirect('resumo_carrinho')

    itens_comprados.update(data_de_compra=datetime.now())
    compra_atual.finalizada = True
    ajusta_estoque(list(itens_comprados))
    compra_atual.data_de_compra = datetime.now()
    compra_atual.save()
    return redirect('feedback')


def instancia_transacao(transacao_form):
    transacao_id = gera_id_transacao()
    endereco = transacao_form.cleaned_data.get('endereco')
    complemento = transacao_form.cleaned_data.get('complemento')
    cidade = transacao_form.cleaned_data.get('cidade')
    bairro = transacao_form.cleaned_data.get('bairro')
    pais = transacao_form.cleaned_data.get('pais')
    estado = transacao_form.cleaned_data.get('estado')
    cep = transacao_form.cleaned_data.get('cep')
    numeroCartao = transacao_form.cleaned_data.get('numeroCartao')
    nomeCartao = transacao_form.cleaned_data.get('nomeCartao')
    mesValidadeCartao = transacao_form.cleaned_data.get('mesValidadeCartao')
    anoValidadeCartao = transacao_form.cleaned_data.get('anoValidadeCartao')
    segurancaCartao = transacao_form.cleaned_data.get('segurancaCartao')
    transacao = Transacao.objects.create(transacao_id=transacao_id, endereco=endereco, complemento=complemento, cidade=cidade,
                                         bairro=bairro, pais=pais, estado=estado, cep=cep, numeroCartao=numeroCartao,
                                         nomeCartao=nomeCartao, mesValidadeCartao=mesValidadeCartao, anoValidadeCartao=anoValidadeCartao, segurancaCartao=segurancaCartao)
    transacao.save()
    return transacao


def ajusta_estoque(lista):
    for item in lista:
        produto = get_object_or_404(Produto, nome_produto=item.produto.nome_produto)
        if item.tamanho == 'G':
            produto.tamanho_grande -= item.quantidade
        elif item.tamanho == 'M':
            produto.tamanho_medio -= item.quantidade
        elif item.tamanho == 'P':
            produto.tamanho_pequeno -= item.quantidade
        if produto.tamanho_pequeno == 0 and produto.tamanho_medio == 0 and produto.tamanho_grande == 0:
            produto.disponibilidade = False
        produto.save()


def verifica_estoque(request, lista):
    for item in lista:
        produto = get_object_or_404(Produto, nome_produto=item.produto.nome_produto)
        if item.tamanho == 'G':
            if item.quantidade > produto.tamanho_grande:
                messages.error(request, '{} tamanho {} indisponível nesta quantidade!'.format(item.produto.nome_produto, item.tamanho))
                return 1
        elif item.tamanho == 'M':
            if item.quantidade > produto.tamanho_medio:
                messages.error(request, '{} tamanho {} indisponível nesta quantidade!'.format(item.produto.nome_produto, item.tamanho))
                return 1
        elif item.tamanho == 'P':
            if item.quantidade > produto.tamanho_pequeno:
                messages.error(request, '{} tamanho {} indisponível nesta quantidade!'.format(item.produto.nome_produto, item.tamanho))
                return 1
    return 0
