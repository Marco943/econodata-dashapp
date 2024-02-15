import dash_mantine_components as dmc
from components.already_logged import already_logged_layout
from dash import (
    Input,
    Output,
    State,
    callback,
    no_update,
    register_page,
)
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify
from flask_login import current_user, login_user
from utils.models import Usuario

register_page(__name__, path="/login", title="Login")


def login_card():
    return dmc.Card(
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
        return dmc.Stack(
            [
                dmc.Title("Bem-vindo!", order=1),
                dmc.Text("Entre na sua conta para continuar", size="sm"),
                login_card(),
            ],
            align="center",
            justify="center",
        )

    else:
        return already_logged_layout


@callback(
    Output("url", "pathname", allow_duplicate=True),
    Output("login-feedback", "children"),
    Output("login-data", "data"),
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
        usuario = Usuario.buscar(email, senha)
    except AssertionError as e:
        return (
            no_update,
            [
                dmc.Alert(
                    "Verifique as credenciais novamente",
                    color="red",
                    variant="outline",
                    mt="1rem",
                    title=str(e),
                )
            ],
            no_update,
        )
    login_user(usuario, remember=remember, force=True)
    return "/user/dashboard", [no_update], 1
