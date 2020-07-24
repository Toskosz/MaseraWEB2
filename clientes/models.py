from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from loja.models import Produto

#User = get_user_model()


class Cliente(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200, default=' ', null=True)
    sobrenome = models.CharField(max_length=200, default=' ', null=True)
    email = models.EmailField(default=None, null=True)
    cpf = models.CharField(max_length=15, default=' ', null=True)
    telefone = models.CharField(max_length=15, default=' ', null=True)
    # produtos = models.ManyToManyField(Produto, blank=True)

    def __str__(self):
        return self.user.username


# Os comandos abaixo serve para que toda vez que um cliente entrar eles tenham um "perfil"

def post_save_cliente_create(sender, instance, created, *args, **kwargs):
    if created:
        Cliente.objects.get_or_create(user=instance)


post_save.connect(post_save_cliente_create, sender=settings.AUTH_USER_MODEL)



