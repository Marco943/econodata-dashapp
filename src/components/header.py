import dash_mantine_components as dmc
from dash import (
    ClientsideFunction,
    Input,
    Output,
    State,
    callback,
    clientside_callback,
    dcc,
    html,
    page_registry,
)
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify
from flask import request
from flask_login import current_user, logout_user
from icecream import ic

ALTURA_HEADER = 60


def header_layout():
    return dmc.Header(
        height=ALTURA_HEADER,
        fixed=True,
        children=[
            dcc.Store(id="login-data", data=0),
            dmc.Grid(
                [
                    dmc.Col(
                        dmc.Anchor(
                            [
                                dmc.Title(
                                    "Econo",
                                    order=2,
                                    color="yellow",
                                    display="inline",
                                ),
                                dmc.Title("data", display="inline", order=2),
                            ],
                            size="xl",
                            href="/",
                            underline=False,
                            variant="text",
                        ),
                        span="content",
                    ),
                    dmc.MediaQuery(
                        dmc.Col(
                            dmc.ActionIcon(
                                DashIconify(icon="radix-icons:hamburger-menu"),
                                id="btn-hamburger",
                            ),
                            id="col-hamburger",
                            span="content",
                        ),
                        largerThan=901,
                        styles={"display": "none"},
                    ),
                    dmc.Col(
                        dmc.Menu(
                            [
                                dmc.MenuTarget(dmc.Button("Páginas", variant="subtle")),
                                dmc.MenuDropdown(
                                    [
                                        dmc.MenuItem(
                                            page["name"] + request.endpoint,
                                            href=page["path"],
                                        )
                                        for page in page_registry.values()
                                    ]
                                ),
                            ]
                        ),
                        span="auto",
                    ),
                    dmc.Col(
                        dmc.Group(
                            [
                                html.Div(id="comp-usr"),
                                dmc.ActionIcon(
                                    DashIconify(icon="gg:dark-mode", width=20),
                                    id="switch-theme",
                                    size=36,
                                    radius=30,
                                ),
                            ]
                        ),
                        span="content",
                    ),
                ],
                justify="space-between",
                align="center",
                style={"height": ALTURA_HEADER, "margin": 0},
            ),
        ],
    )


clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="abrir_hamburger_menu"),
    Output("drawer-navbar", "opened"),
    Input("btn-hamburger", "n_clicks"),
    prevent_initial_call=True,
)

clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="carregar_tema_cache"),
    Output("mantine-main-provider", "theme"),
    Input("theme-store", "data"),
)

clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="trocar_tema"),
    Output("theme-store", "data"),
    Input("switch-theme", "n_clicks"),
    State("theme-store", "data"),
)


@callback(Output("comp-usr", "children"), Input("login-data", "data"))
def construir_user_header(_):
    if current_user.is_authenticated:
        user_status_layout = dmc.Menu(
            [
                dmc.MenuTarget(
                    dmc.Button(
                        current_user.nome,
                        variant="light",
                        rightIcon=DashIconify(icon="bxs:down-arrow"),
                    )
                ),
                dmc.MenuDropdown(
                    [
                        dmc.MenuItem(
                            "Configurações",
                            icon=DashIconify(icon="solar:settings-bold"),
                            href="/user/configuracoes",
                        ),
                        dmc.MenuDivider(),
                        dmc.MenuItem(
                            "Sair",
                            id="logout-header-btn",
                            icon=DashIconify(icon="bxs:exit"),
                        ),
                    ]
                ),
            ]
        )
    else:
        user_status_layout = html.Div()
    return user_status_layout


@callback(
    Output("refresh", "data", allow_duplicate=True),
    Input("logout-header-btn", "n_clicks"),
    prevent_initial_call=True,
)
def logout(n_clicks):
    if n_clicks:
        logout_user()
        # Força um refresh
        return 1
    else:
        raise PreventUpdate
