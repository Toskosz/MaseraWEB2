from django.db import models
from django.utils.translation import gettext_lazy as _


class Estados(models.TextChoices):
    DF = 'DF', _('DF')
    RJ = 'RJ', _('RJ')
    SP = 'SP', _('SP')


# class MesValidade(models.TextChoices):
mes_choices = [
    (str(i), str(i)) for i in range(1, 12)
]


# class AnoValidade(models.TextChoices):
ano_choices = [
    (str(i), str(i)) for i in range(20, 40)
]
