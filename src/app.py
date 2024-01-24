import os

import dash_mantine_components as dmc
from components.header import header_layout
from components.navbar import drawer_navbar_layout, navbar_layout
from dash import Dash, dcc, html, page_container
from dotenv import load_dotenv
from flask import Flask
from flask_login import current_user
from utils.models import login_manager, mongo

load_dotenv(override=True)

server = Flask(__name__)
server.config.update(SECRET_KEY=os.environ.get("SECRET_KEY"))
server.config.update(MONGO_URI=os.environ.get("DB_ECONODATA"))

mongo.init_app(server)
login_manager.init_app(server)

app = Dash(
    use_pages=True,
    suppress_callback_exceptions=True,
    title="App Econodata",
    update_title=None,
    server=server,
    prevent_initial_callbacks=True,
)


def app_layout():
    return dmc.MantineProvider(
        [
            dcc.Store(id="theme-store", storage_type="local"),
            dcc.Location(id="url", refresh=True),
            dmc.NotificationsProvider(
                [
                    html.Div(
                        dmc.Container(
                            [
                                header_layout(),
                                navbar_layout(),
                                drawer_navbar_layout(),
                                html.Div(page_container, id="content"),
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


app.layout = app_layout

if __name__ == "__main__":
    # app.run(debug=True)
    server.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
