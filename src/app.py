import locale
import os

import dash_mantine_components as dmc
from components.header import header_layout
from components.navbar import drawer_navbar_layout, navbar_layout
from dash import (
    ClientsideFunction,
    Dash,
    Input,
    Output,
    clientside_callback,
    dcc,
    html,
    page_container,
)
from dotenv import load_dotenv
from flask import Flask
from utils.models import cache, login_manager, mail, mongo

locale.setlocale(locale.LC_ALL, "pt_br.utf8")

load_dotenv(override=True)

server = Flask(__name__)
server.config.from_prefixed_env()

mongo.init_app(server)
login_manager.init_app(server)
mail.init_app(server)
cache.init_app(server)

app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    title="App Econodata",
    update_title=None,
    server=server,
    prevent_initial_callbacks=True,
    external_scripts=[
        "https://cdn.plot.ly/plotly-locale-pt-br-latest.js",
        "https://cdnjs.cloudflare.com/ajax/libs/dayjs/1.11.10/dayjs.min.js",
        "https://cdnjs.cloudflare.com/ajax/libs/dayjs/1.11.10/locale/pt-br.min.js",
    ],
)


def app_layout():
    return dmc.MantineProvider(
        [
            dcc.Store(id="login-data", data=0),
            dcc.Store(id="refresh", data=0),
            dcc.Store(id="theme-store", storage_type="local"),
            dcc.Location(id="url", refresh=True),
            dmc.NotificationsProvider(
                children=dmc.Container(
                    [
                        header_layout(),
                        navbar_layout(),
                        drawer_navbar_layout(),
                        html.Div(page_container, id="content"),
                    ],
                    fluid=True,
                    px=0,
                )
            ),
        ],
        theme={"colorScheme": "light", "primaryColor": "yellow"},
        id="mantine-main-provider",
        inherit=True,
        withGlobalStyles=True,
        withNormalizeCSS=True,
    )


app.layout = app_layout

clientside_callback(
    ClientsideFunction("clientside", "atualizar_pagina"),
    Output("refresh", "data"),
    Input("refresh", "data"),
    prevent_initial_call=True,
)

if __name__ == "__main__":
    # app.run(debug=True)
    server.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
