from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', include('loja.urls')),
    path('carrinho/', include('carrinho.urls')),
    path('cliente/', include('clientes.urls')),
    path('admin/', admin.site.urls),
    path('transacao/', include('transacao.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

