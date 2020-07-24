from django.conf import settings
from django.contrib import messages, auth
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from clientes.models import Cliente
from loja.models import Produto
from carrinho.extras import gera_id_compra
from carrinho.models import ItemCompra, Compra


def atual_compra_pendente(request):
    cliente = get_object_or_404(Cliente, user=request.user)
    compra = Compra.objects.filter(comprador=cliente, finalizada=False)
    if compra.exists():
        return compra[0]
    return 0


@login_required()
def add_produto_carrinho(request, produto_id):
    # pega perfil do usuario
    usuario = get_object_or_404(Cliente, user=request.user)

    # filtra produto selecionado por id
    produto = Produto.objects.filter(pk=produto_id).first()

    # Atribui o tamanho e quantidade selecionada
    tamanho = request.POST.get('tamanho', 'x')

    # Cria a ordem do item selecionado
    item_compra, status = ItemCompra.objects.get_or_create(cliente=usuario, produto=produto, tamanho=tamanho)

    item_compra.quantidade += 1
    item_compra.save()

    # create compra associada ao usuario
    compra_usuario, status = Compra.objects.get_or_create(comprador=usuario, finalizada=False)

    compra_usuario.itens.add(item_compra)
    compra_usuario.total += produto.preco
    if status:
        # gera codigo de referencia da compra
        compra_usuario.codigo_de_referencia = gera_id_compra()
    compra_usuario.save()

    # mensagem de confirmação
    messages.success(request, 'Item adicionado ao carrinho')
    return redirect('index')


@login_required()
def deleta_produto_carrinho(request, item_compra_id):
    compra_atual = atual_compra_pendente(request)
    item_to_delete = ItemCompra.objects.filter(pk=item_compra_id).first()
    if item_to_delete and item_to_delete.quantidade == 1:
        item_to_delete.delete()
        messages.info(request, "Item removido do carrinho")
    else:
        item_to_delete.quantidade -= 1
        item_to_delete.save()
    compra_atual.total -= item_to_delete.produto.preco
    compra_atual.save()
    return redirect('resumo_carrinho')


@login_required()
def resumo_carrinho(request):
    compra_atual = atual_compra_pendente(request)
    if compra_atual == 0:
        return render(request, 'carrinho/carrinho.html')
    else:
        itens = list(compra_atual.get_itens_carrinho())
        total = compra_atual.total
        dados = {
            'order': itens,
            'total': total
        }
        return render(request, 'carrinho/carrinho.html', dados)
