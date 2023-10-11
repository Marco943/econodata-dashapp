from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, username, email, password, _id=None):
        self.username = username
        self.email = email
        self.password = password
        self.id = _id

    @staticmethod
    def check_password():
        ...
