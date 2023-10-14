from flask_login import UserMixin
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash

mongo = PyMongo()


class User(UserMixin):
    def __init__(self, _id, username=None, email=None, password=None):
        self.id = str(_id)
        self.username = username
        self.email = email
        self.password = password

    def register_user(self):
        if not mongo.db["Users"].find_one({"name": self.email}):
            mongo.db["Users"].insert_one(
                {
                    "name": self.username,
                    "email": self.email,
                    "password": generate_password_hash(self.password),
                    "admin": 0,
                }
            )
            return "success"
        return "fail"
