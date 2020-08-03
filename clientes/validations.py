from email_validator import validate_email, EmailNotValidError


def digitos_verificadores_cpf_errados(cpf):
    cpf_temp = cpf[::-1]
    cpf_temp = cpf_temp[2:]
    cpf_temp = [int(x) for x in cpf_temp]
    v1 = 0
    v2 = 0
    for i in range(0, 9):
        v1 = v1 + cpf_temp[i] * (9 - (i % 10))
        v2 = v2 + cpf_temp[i] * (9 - ((i+1) % 10))
    v1 = ( v1 % 11) % 10
    v2 = v2 + v1 * 9
    v2 = (v2 % 11) % 10
    if str(v1) != cpf[-2] or str(v2) != cpf[-1]:
        return 1
    else:
        return 0


def valida_cpf(valor_campo, nome_campo, lista_de_erros):
    if not valor_campo.isdigit():
        lista_de_erros[nome_campo] = 'Insira apenas os números do CPF'
        return
    if len(valor_campo) != 11:
        lista_de_erros[nome_campo] = 'Quantidade de caracteres inválida'
        return
    if digitos_verificadores_cpf_errados(valor_campo):
        lista_de_erros[nome_campo] = 'CPF inválido'
        return


def email_invalido(valor_campo, nome_campo, lista_de_erros):
    try:
        valido = validate_email(valor_campo)
    except EmailNotValidError as e:
        lista_de_erros[nome_campo] = 'Email inválido'