import re
from typing import Any, Optional

from flask_login import LoginManager, UserMixin, login_user
from flask_pymongo import ObjectId, PyMongo
from pydantic import BaseModel, computed_field, field_validator
from werkzeug.security import check_password_hash, generate_password_hash

mongo = PyMongo()

login_manager = LoginManager()
login_manager.login_view = "/"


class NovoUsuario(BaseModel):
    nome: Optional[str] = None
    sobrenome: Optional[str] = None
    cpf: Optional[str] = None
    email: Optional[str] = None
    senha: Optional[str] = None
    senha_check: Optional[str] = None

    @field_validator("*")
    @classmethod
    def em_branco(cls, v: Any, field) -> Any:
        if not v:
            raise ValueError(f"O campo '{field.field_name}' é obrigatório.")
        return v

    @field_validator("email")
    @classmethod
    def email_valido(cls, email: str) -> str:
        if not re.compile(
            "([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
        ).fullmatch(email):
            raise ValueError("Email inválido")
        return email

    @field_validator("cpf")
    @classmethod
    def validar_cpf(cls, cpf: str) -> str:
        if len(cpf) != 11 or not (all(map(str.isdigit, cpf))):
            raise ValueError("CPF inválido")
        cpf_digitos = tuple(map(int, cpf))
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
        if not (condicao1_1 or condicao1_2 or condicao2_1 or condicao2_2):
            raise ValueError("CPF inválido")
        return cpf

    @field_validator("senha")
    @classmethod
    def validar_senha(cls, senha: str) -> str:
        if not re.compile(
            "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,}$"
        ).fullmatch(senha):
            raise ValueError("Senha fraca")
        return senha

    @field_validator("senha_check")
    @classmethod
    def senhas_combinam(cls, senha_check: str, info) -> str:
        if "senha" in info.data and senha_check != info.data["senha"]:
            raise ValueError("As senhas não combinam")
        return senha_check

    def registrar(self) -> bool:
        if mongo.db["Users"].find_one({"email": self.email}):
            return False
        mongo.db["Users"].insert_one(
            {
                "nome": self.nome,
                "sobrenome": self.sobrenome,
                "cpf": self.cpf,
                "email": self.email,
                "senha": generate_password_hash(self.senha),
                "admin": False,
                "membro": False,
            }
        )
        return True


class Usuario(BaseModel, UserMixin):
    _id: Optional[ObjectId] = None
    nome: Optional[str] = None
    sobrenome: Optional[str] = None
    cpf: Optional[str] = None
    email: Optional[str] = None

    @computed_field
    @property
    def id(self) -> str:
        return str(self._id)

    def buscar(self, email: str, senha: str):
        usuario = mongo.db["Users"].find_one(
            {"email": email},
            {campo: 1 for campo in ["nome", "sobrenome", "cpf", "email", "senha"]},
        )
        if not usuario:
            raise ValueError("Usuário não encontrado")
        if not check_password_hash(usuario["senha"], senha):
            raise ValueError("Senha incorreta")
        self._id = usuario["_id"]
        self.nome = usuario["nome"]
        self.sobrenome = usuario["sobrenome"]
        self.cpf = usuario["cpf"]
        self.email = usuario["email"]
        self.nome = "teste"
        return self


@login_manager.user_loader
def load_user(user_id):
    user = mongo.db["Users"].find_one(
        {"_id": ObjectId(user_id)},
    )
    if not user:
        return None
    return Usuario(**user)
