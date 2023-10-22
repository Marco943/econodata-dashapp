import os
from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager, current_user
from flask_pymongo import ObjectId
from dash import Dash, html, dcc, page_container, callback, Output, Input
import dash_mantine_components as dmc

from utils.models import mongo, User
from components.header import header_layout, ALTURA_HEADER
from components.navbar import navbar_layout, drawer_navbar_layout, LARGURA_NAVBAR
from icecream import ic

server = Flask(__name__)
load_dotenv(override=True)
server.config.update(SECRET_KEY=os.environ.get("SECRET_KEY"))
server.config.update(MONGO_URI=os.environ.get("DB_ECONODATA"))

mongo.init_app(server)

login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = "/login"

app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    title="App Econodata",
    update_title=None,
    server=server,
    prevent_initial_callbacks=True,
)


@login_manager.user_loader
def load_user(user_id):
    user = mongo.db["Users"].find_one(
        {"_id": ObjectId(user_id)},
        {campo: 1 for campo in ["nome", "sobrenome", "cpf", "email"]},
    )
    if not user:
        return None
    return User(
        user["_id"], user["nome"], user["sobrenome"], user["cpf"], user["email"], None
    )


app.layout = dmc.MantineProvider(
    [
        dcc.Store(id="theme-store", storage_type="session"),
        dcc.Location(id="url", refresh="callback-nav"),
        dmc.NotificationsProvider(
            [
                html.Div(
                    dmc.Container(
                        [
                            header_layout,
                            navbar_layout(),
                            drawer_navbar_layout(),
                            html.Div(
                                dmc.Container(
                                    page_container,
                                    size="lg",
                                    pt=ALTURA_HEADER + 20,
                                ),
                                id="wrapper",
                            ),
                        ],
                        fluid=True,
                        px=0,
                    ),
                    style={"height": "100vh"},
                )
            ]
        ),
    ],
    theme={"colorScheme": "light", "primaryColor": "yellow"},
    id="mantine-main-provider",
    inherit=True,
    withGlobalStyles=True,
    withNormalizeCSS=True,
)


if __name__ == "__main__":
    # app.run(debug=True)
    server.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
