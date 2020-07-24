import random
import string
from datetime import date
import datetime


def gera_id_transacao():
    date_str = date.today().strftime('%d%m%Y')[2:] + str(datetime.datetime.now().microsecond)
    rand_str = "".join([random.choice(string.digits) for count in range(3)])
    return date_str + rand_str
