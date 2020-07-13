from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from .models import Produto
from django.contrib.auth.decorators import login_required


@login_required()
def index(request):
    produtos = Produto.objects.filter(publicado=True)
    dados = {
        'produtos': produtos
    }
    return render(request, 'index.html', dados)


def sobre(request):
    return render(request, 'sobre.html')


def produto(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    produto_a_exibir = {
        'produto': produto
    }
    return render(request, 'produto.html', produto_a_exibir)

