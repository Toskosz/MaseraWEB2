from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sobre', views.sobre, name='sobre'),
    path('produto/<str:produto_nome_url>', views.produto, name='produto')
]
