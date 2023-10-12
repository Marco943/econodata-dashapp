from dash import Dash, html, dcc, page_container
import dash_mantine_components as dmc
from flask_login import LoginManager
from flask import Flask
import os
from utils.models import mongo, User

server = Flask(__name__)

server.config.update(SECRET_KEY=os.getenv("SECRET_KEY"))
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
)


@login_manager.user_loader
def load_user(username):
    user = mongo.db["Users"].find_one({"name": username})
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


if __name__ == "__main__":
    app.run(debug=True)
