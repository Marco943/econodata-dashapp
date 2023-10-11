from dash import Dash, html, dcc, page_container, Input, Output, State, callback
import dash_mantine_components as dmc
from flask_login import LoginManager, UserMixin
from flask_pymongo import PyMongo
import os

# from flask_sqlalchemy import SQLAlchemy

app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    title="App Econodata",
    update_title=None,
)
server = app.server
server.config.update(SECRET_KEY=os.getenv("SECRET_KEY"))
server.config.update(MONGO_URI=os.getenv("DB_USERS"))

mongo = PyMongo(server)

login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = "/login"


class User(UserMixin):
    def __init__(self, username, email, password, _id=None):
        self.username = username
        self.email = email
        self.password = password
        self.id = _id


# db.init_app(server)
# with server.app_context():
#     db.create_all()


@login_manager.user_loader
def load_user(username):
    user = mongo.db.Users.find_one({"name": username})
    if not user:
        return None
    return User(username=user["name"])


app.layout = dmc.MantineProvider(
    [
        dcc.Store(id="theme-store", storage_type="local"),
        dcc.Location(id="url", refresh="callback-nav"),
        dmc.NotificationsProvider(
            [
                html.Div(
                    dmc.Container(page_container, fluid=True), style={"height": "100vh"}
                )
            ]
        ),
    ],
    theme={"colorScheme": "light"},
    id="mantine-main-provider",
    inherit=True,
    withGlobalStyles=True,
)


@callback(
    Output("register-info", "value"),
    State("register-in-user", "value"),
    State("register-in-email", "value"),
    State("register-in-pwd", "value"),
    State("register-in-pwd2", "value"),
    Input("register-btn", "n_clicks"),
    prevent_initial_call=True,
)
def register_new_user(username, email, pwd, pwd2, n):
    if n and username and email and pwd and pwd2:
        mongo.db.Users.insert_one({"name": username, "email": email, "password": pwd})
        print("registrado")
        return "registrado"


if __name__ == "__main__":
    app.run(debug=True)
