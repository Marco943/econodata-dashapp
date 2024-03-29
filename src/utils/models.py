import re
from typing import Any, Optional

from flask_caching import Cache
from flask_login import LoginManager, UserMixin
from flask_mail import Mail
from flask_pymongo import ObjectId, PyMongo
from pydantic import BaseModel, Field, computed_field, field_validator
from werkzeug.security import check_password_hash, generate_password_hash

mongo = PyMongo()

login_manager = LoginManager()
login_manager.login_view = "/"

mail = Mail()

cache = Cache()


class NovoUsuario(BaseModel):
    nome: str
    sobrenome: str
    cpf: str
    email: str
    senha: str
    senha_check: str

    @field_validator("*", mode="before")
    @classmethod
    def em_branco(cls, v: Any, field) -> Any:
        assert bool(v), "Todos os campos marcados com (*) são obrigatórios"
        return v

    @field_validator("email")
    @classmethod
    def email_valido(cls, email: str) -> str:
        assert re.compile(
            r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
        ).fullmatch(email), "Email inválido"
        return email

    @field_validator("cpf")
    @classmethod
    def validar_cpf(cls, cpf: str) -> str:
        assert len(cpf) == 11 and cpf.isdigit(), "CPF inválido"
        cpf_d = tuple(map(int, cpf))
        resto1 = sum(((10 - i) * n for i, n in enumerate(cpf_d[:9]))) % 11
        regra1 = (resto1 <= 1 and cpf_d[-2] == 0) or (
            resto1 >= 2 and cpf_d[-2] == 11 - resto1
        )
        resto2 = sum(((11 - i) * n for i, n in enumerate(cpf_d[:10]))) % 11
        regra2 = (resto2 <= 1 and cpf_d[-1] == 0) or (
            resto2 >= 2 and cpf_d[-1] == 11 - resto2
        )
        assert regra1 and regra2, "CPF inválido"
        return cpf

    @field_validator("senha")
    @classmethod
    def validar_senha(cls, senha: str) -> str:
        assert re.compile(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,}$"
        ).fullmatch(senha), "Senha fraca"
        return senha

    @field_validator("senha_check")
    @classmethod
    def senhas_combinam(cls, senha_check: str, info) -> str:
        assert info.data["senha"] == senha_check, "As senhas não são iguais"
        return senha_check

    def registrar(self) -> bool:
        assert not mongo.db["Users"].find_one(
            {"cpf": self.cpf}
        ), "Este CPF já foi cadastrado"
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
    id_: ObjectId = Field(alias="_id")
    nome: str
    sobrenome: str
    cpf: str
    email: str

    class Config:
        arbitrary_types_allowed = True

    @computed_field
    @property
    def id(self) -> str:
        return str(self.id_)

    @classmethod
    def buscar(cls, email: str, senha: str):
        assert email != "" and senha != "", "Preencha todos os campos"
        usuario = mongo.db["Users"].find_one(
            {"email": email},
            {campo: 1 for campo in ["nome", "sobrenome", "cpf", "email", "senha"]},
        )
        assert usuario, "Usuário não encontrado"
        assert check_password_hash(usuario["senha"], senha), "Senha incorreta"

        return cls(**usuario)

    def alterar_senha(
        self, senha_atual: str, senha_nova: str, senha_nova_check: str
    ) -> bool:
        senha_hash = mongo.db["Users"].find_one(
            {"_id": self.id_}, {"_id": 0, "senha_hash": 1}
        )["senha_hash"]
        assert check_password_hash(
            senha_hash, senha_atual
        ), "A senha atual não está correta."

        assert not check_password_hash(
            senha_hash, senha_nova
        ), "A senha nova não pode ser igual à senha atual."

        assert (
            senha_nova == senha_nova_check
        ), "As senhas novas inseridas não são iguais."

        r = mongo.db["Users"].update_one(
            {"_id": self.id_},
            {"$set": {"senha_hash": generate_password_hash(senha_nova)}},
        )
        assert r.acknowledged, "Ocorreu algum problema, tente novamente mais tarde."
        return True


@login_manager.user_loader
def load_user(user_id):
    user = mongo.db["Users"].find_one(
        {"_id": ObjectId(user_id)},
    )
    if not user:
        return None
    return Usuario(**user)
