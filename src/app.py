from dash import Dash, html, dcc, page_container, callback, Output, Input
import dash_mantine_components as dmc
from flask_login import LoginManager, current_user
from flask import Flask
from flask_pymongo import ObjectId
import os
from dotenv import dotenv_values, find_dotenv
from utils.models import mongo, User
from components.header import header_layout, ALTURA_HEADER
from components.navbar import navbar_layout, LARGURA_NAVBAR
from icecream import ic

server = Flask(__name__)

server.config.update(SECRET_KEY="chavemegasecreta")
server.config.update(
    MONGO_URI="mongodb+srv://Marco:efp6It13de0zJO8w@cluster0.lcdcwit.mongodb.net/Econodata?retryWrites=true&w=majority"
)

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
    user = mongo.db["Users"].find_one({"_id": ObjectId(user_id)})
    if not user:
        return None
    return User(_id=user["_id"], username=user["name"], email=user["email"])


app.layout = dmc.MantineProvider(
    [
        dcc.Store(id="theme-store", storage_type="local"),
        dcc.Location(id="url", refresh="callback-nav"),
        dmc.NotificationsProvider(
            [
                html.Div(
                    dmc.Container(
                        [
                            header_layout,
                            navbar_layout,
                            html.Div(
                                page_container,
                                style={
                                    "padding-top": ALTURA_HEADER + 20,
                                    "padding-left": LARGURA_NAVBAR + 20,
                                },
                            ),
                        ],
                        fluid=True,
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
    app.run(debug=True)
