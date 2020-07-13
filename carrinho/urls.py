from django.urls import path
from . import views

urlpatterns = [
    path('add-ao-carrinho/<int:produto_id>', views.add_produto_carrinho, name='add_produto_carrinho'),
    path('deleta-do-carrinho/<int:item_compra_id>', views.deleta_produto_carrinho, name='deleta_produto_carrinho'),
    path('finaliza-compra', views.finaliza_compra, name='finaliza_compra'),
    path('resumo', views.resumo_carrinho, name='resumo_carrinho'),
    path('checkout', views.checkout, name='checkout'),
    path('feedback', views.feedback, name='feedback'),
]