import re

RE_EMAIL = re.compile(
    "([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
)

RE_SENHA = re.compile(
    "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,}$"
)

RE_CPF = re.compile("")


def validar_email(email: str) -> bool:
    if RE_EMAIL.fullmatch(email):
        return True
    else:
        return False


def validar_senha(senha: str) -> bool:
    if RE_SENHA.fullmatch(senha):
        return True
    else:
        return False


def validar_cpf(cpf: str) -> bool:
    if len(cpf) == 11 and all(map(str.isdigit, cpf)):
        cpf_digitos = [int(i) for i in cpf]
        resto1 = (
            sum([digito * (10 - i) for i, digito in enumerate(cpf_digitos[0:9])]) % 11
        )
        resto2 = (
            sum([digito * (11 - i) for i, digito in enumerate(cpf_digitos[0:10])]) % 11
        )
        condicao1_1 = resto1 <= 1 and cpf_digitos[-2] == 0
        condicao1_2 = resto1 > 2 and cpf_digitos[-2] == (11 - resto1)
        condicao2_1 = resto2 <= 1 and cpf_digitos[-1] == 0
        condicao2_2 = resto2 > 2 and cpf_digitos[-1] == (11 - resto2)
        if condicao1_1 or condicao1_2 or condicao2_1 or condicao2_2:
            return True
    return False
