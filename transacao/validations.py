def campo_vazio(valor_campo, nome_campo, lista_de_erros):
    if not valor_campo:
        lista_de_erros[nome_campo] = 'Não deixe campos em branco.'
        return 1
    return 0


def campo_tem_numero(valor_campo, nome_campo, lista_de_erros):
    if any(char.isdigit() for char in valor_campo):
        lista_de_erros[nome_campo] = 'Não inclua números neste campo.'


def campo_tem_letra(valor_campo, nome_campo, lista_de_erros):
    if any(char.isalpha() for char in valor_campo):
        lista_de_erros[nome_campo] = 'Não inclua letras neste campo.'