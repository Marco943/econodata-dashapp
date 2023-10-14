import dash_mantine_components as dmc
from dash import callback, Output, Input, Patch, html
from dash.exceptions import PreventUpdate
from flask_login import current_user
from icecream import ic


def build_user_header():
    if current_user.is_authenticated:
        user_status_layout = dmc.Text(f"Olá, {current_user.username}")
    else:
        user_status_layout = dmc.Button("Login", id="btn-goto-login")
    return user_status_layout


header_layout = dmc.Header(
    dmc.Stack(
        [
            dmc.Grid(
                [
                    dmc.Col([dmc.Text("Econodata")], span="content"),
                    dmc.Col(
                        dmc.Group(
                            [
                                html.Div(id="component-user-header"),
                                dmc.Switch(
                                    "Modo Escuro/Claro",
                                    id="switch-dark-light",
                                    checked=True,
                                ),
                            ]
                        ),
                        span="content",
                    ),
                ],
                justify="space-between",
            )
        ],
        justify="center",
    ),
    height=60,
    fixed=True,
)


@callback(
    Output("mantine-main-provider", "theme"), Input("switch-dark-light", "checked")
)
def trocar_tema(checked):
    patched_theme = Patch()
    if checked:
        patched_theme["colorScheme"] = "light"
    else:
        patched_theme["colorScheme"] = "dark"
    return patched_theme


@callback(
    Output("url", "pathname", allow_duplicate=True),
    Input("btn-goto-login", "n_clicks"),
    prevent_initial_call=True,
)
def redirecionar(n_clicks):
    if n_clicks:
        return "/login"
    else:
        raise PreventUpdate


@callback(Output("component-user-header", "children"), Input("url", "pathname"))
def update_user_header(url):
    return build_user_header()
