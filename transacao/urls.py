from django.urls import path
from . import views


urlpatterns = [
    path('checkout', views.checkout, name='checkout'),
    path('feedback', views.feedback, name='feedback'),
    path('cofirma-compra', views.cofirma_compra, name='cofirma_compra'),
    path('finaliza-compra', views.finaliza_compra, name='finaliza_compra')
    ]