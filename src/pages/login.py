from dash import html, callback, register_page, Output, Input, State, no_update
from dash.exceptions import PreventUpdate
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from flask_login import login_user, current_user
from werkzeug.security import check_password_hash
from icecream import ic
from utils.models import mongo, User
from components.already_logged import already_logged_layout

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
def login(n_clicks, email, password, remember):
    if n_clicks:
        find_user = mongo.db["Users"].find_one(
            {"email": email},
            {campo: 1 for campo in ["nome", "sobrenome", "cpf", "email", "senha"]},
        )
        if not find_user:
            return no_update, [
                dmc.Alert("Usuário não encontrado!", color="red", variant="filled")
            ]
        if not check_password_hash(find_user["senha"], password):
            return no_update, [
                dmc.Alert("Senha incorreta!", color="red", variant="filled")
            ]
        else:
            user = User(
                find_user["_id"],
                find_user["nome"],
                find_user["sobrenome"],
                find_user["cpf"],
                find_user["email"],
                None,
            )
            login_user(user, remember=remember, force=True)
            return "/user/dashboard", [
                dmc.Alert("Logado com sucesso!", color="green", variant="filled")
            ]
    else:
        raise PreventUpdate
