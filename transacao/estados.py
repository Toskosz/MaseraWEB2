from django.db import models
from django.utils.translation import gettext_lazy as _


class Estados(models.TextChoices):
    DF = 'DF', _('DF')
    RJ = 'RJ', _('RJ')
    SP = 'SP', _('SP')