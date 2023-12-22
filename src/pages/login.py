import dash_mantine_components as dmc
from components.already_logged import already_logged_layout
from dash import (
    Input,
    Output,
    State,
    callback,
    clientside_callback,
    html,
    no_update,
    register_page,
)
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify
from flask_login import current_user, login_user
from icecream import ic
from pydantic import ValidationError
from utils.models import Usuario, mongo
from werkzeug.security import check_password_hash

register_page(__name__, path="/login", title="Login")

login_card = dmc.Card(
    [
        dmc.CardSection(
            [
                dmc.TextInput(
                    id="login-in-email",
                    type="email",
                    label="Email",
                    icon=DashIconify(icon="ic:round-alternate-email"),
                ),
                dmc.PasswordInput(
                    id="login-in-pwd",
                    label="Senha",
                    icon=DashIconify(icon="carbon:password"),
                ),
                dmc.Checkbox(
                    id="login-chk-remember",
                    label="Lembar de mim",
                    checked=False,
                    pt="1rem",
                ),
                dmc.Button(
                    "Conectar-se",
                    id="login-btn",
                    fullWidth=True,
                    mt="1rem",
                    variant="solid",
                    n_clicks=0,
                ),
                dmc.Group(
                    [
                        dmc.Text("Não tem conta?", size=12),
                        dmc.Anchor("Crie uma", href="/signup", size=12),
                    ],
                    spacing=5,
                    position="center",
                    mt="0.5rem",
                ),
                dmc.Text(id="login-feedback"),
            ]
        )
    ],
    p="1rem",
    w=350,
)


def layout():
    if not current_user.is_authenticated:
        return html.Div(
            [
                dmc.Title("Bem-vindo!", order=1),
                dmc.Text("Entre na sua conta para continuar", size="sm"),
                login_card,
            ]
        )
    else:
        return already_logged_layout


@callback(
    Output("url", "pathname", allow_duplicate=True),
    Output("login-feedback", "children"),
    Input("login-btn", "n_clicks"),
    State("login-in-email", "value"),
    State("login-in-pwd", "value"),
    State("login-chk-remember", "checked"),
    prevent_initial_call=True,
)
def login(n_clicks, email, senha, remember):
    if not n_clicks:
        raise PreventUpdate
    try:
        usuario = Usuario().buscar(email, senha)
    except ValidationError as e:
        return no_update, [
            dmc.Alert(e.errors()[0]["msg"], color="red", variant="filled", mt="1rem")
        ]
    login_user(usuario, remember=remember, force=True)
    return "/user/dashboard", [no_update]
