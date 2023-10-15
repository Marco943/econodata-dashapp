from flask_login import UserMixin
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash

mongo = PyMongo()


class User(UserMixin):
    def __init__(
        self, _id=None, nome=None, sobrenome=None, cpf=None, email=None, senha=None
    ):
        self.id = str(_id)
        self.nome = nome
        self.sobrenome = sobrenome
        self.cpf = cpf
        self.email = email
        self.senha = senha

    def signup(self) -> bool:
        if not mongo.db["Users"].find_one({"email": self.email}):
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
        return False
