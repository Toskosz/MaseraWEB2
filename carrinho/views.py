from django.conf import settings
from django.contrib import messages, auth
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from clientes.models import Cliente
from loja.models import Produto
import datetime
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
    if status:
        # gera codigo de referencia da compra
        compra_usuario.ref_code = gera_id_compra()
        compra_usuario.save()

    # mensagem de confirmação
    messages.success(request, 'Item adicionado ao carrinho')
    return redirect('index')


@login_required()
def deleta_produto_carrinho(request, item_compra_id):
    item_to_delete = ItemCompra.objects.filter(pk=item_compra_id).first()
    if item_to_delete and item_to_delete.quantidade == 1:
        item_to_delete.delete()
        messages.info(request, "Item removido do carrinho")
    else:
        item_to_delete.quantidade -= 1
        item_to_delete.save()
    return redirect('resumo_carrinho')


@login_required()
def resumo_carrinho(request):
    compra_atual = atual_compra_pendente(request)
    if compra_atual == 0:
        return render(request, 'carrinho.html')
    else:
        itens = list(compra_atual.get_itens_carrinho())
        total = compra_atual.get_total_carrinho()
        dados = {
            'order': itens,
            'total': total
        }
        return render(request, 'carrinho.html', dados)


@login_required()
def checkout(request, **kwargs):
    compra = atual_compra_pendente(request)
    itens = list(compra.get_itens_carrinho())
    total = compra.get_total_carrinho()
    dados = {
        'order': itens,
        'total': total,
    }
    return render(request, 'checkout.html', dados)


@login_required()
def finaliza_compra(request):
    compra_atual = atual_compra_pendente(request)
    itens_comprados = compra_atual.get_itens_carrinho()

    if not ajusta_estoque(request, list(itens_comprados)):
        return redirect('resumo_carrinho')
    else:
        cliente_temp = get_object_or_404(Cliente, user=request.user)
        cliente_final = Cliente.objects.filter(email=request.POST['email']).first()
        if cliente_final:
            compra_atual.comprador = cliente_final
            itens_comprados.update(cliente=cliente_final, data_de_compra=datetime.datetime.now())
            usuario_anterior = request.user
            request.user = cliente_final.user
            usuario_anterior.delete()
            cliente_temp.delete()
        else:
            cliente_temp.nome = request.POST['nome']
            cliente_temp.sobrenome = request.POST['sobrenome']
            cliente_temp.email = request.POST['email']
            request.user.username = request.POST['email']
            itens_comprados.update(data_de_compra=datetime.datetime.now())
            request.user.save()
            cliente_temp.save()

        compra_atual.finalizada = True
        compra_atual.data_de_compra = datetime.datetime.now()
        compra_atual.save()

        return redirect('feedback')


@login_required()
def feedback(request, **kwargs):
    auth.logout(request)
    return render(request, 'feedback.html')


def ajusta_estoque(request, lista):
    for item in lista:
        produto = get_object_or_404(Produto, nome_produto=item.produto.nome_produto)
        if item.tamanho == 'G':
            if item.quantidade > produto.tamanho_grande:
                messages.error(request, '{} tamanho {} indisponível nesta quantidade!'.format(item.produto.nome_produto, item.tamanho))
                return 0
            else:
                produto.tamanho_grande -= item.quantidade
                produto.save()
        elif item.tamanho == 'M':
            if item.quantidade > produto.tamanho_medio:
                messages.error(request, '{} tamanho {} indisponível nesta quantidade!'.format(item.produto.nome_produto, item.tamanho))
                return 0
            else:
                produto.tamanho_medio -= item.quantidade
                produto.save()
        elif item.tamanho == 'P':
            if item.quantidade > produto.tamanho_pequeno:
                messages.error(request, '{} tamanho {} indisponível nesta quantidade!'.format(item.produto.nome_produto, item.tamanho))
                return 0
            else:
                produto.tamanho_pequeno -= item.quantidade
                produto.save()

        if produto.tamanho_pequeno == 0 and produto.tamanho_medio == 0 and produto.tamanho_grande == 0:
            produto.disponibilidade = False
            produto.publicado = False
            produto.save()
    return 1


def campo_vazio(campo):
    return not campo.strip()
