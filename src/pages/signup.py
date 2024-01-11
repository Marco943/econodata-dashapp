import dash_mantine_components as dmc
from components.already_logged import already_logged_layout
from dash import Input, Output, State, callback, html, register_page
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify
from flask_login import current_user
from pydantic import ValidationError
from utils.models import NovoUsuario, Usuario

register_page(__name__, path="/signup", title="Criar uma conta")

signup_card = [
    dmc.Card(
        [
            dmc.CardSection(
                [
                    dmc.Title("Criar uma conta", order=4, ta="center"),
                    dmc.TextInput(
                        id="signup-submit-nome",
                        type="text",
                        label="Nome",
                        placeholder="Fulano",
                        required=True,
                    ),
                    dmc.TextInput(
                        id="signup-submit-sobrenome",
                        type="text",
                        label="Sobrenome",
                        placeholder="da Silva",
                        required=True,
                    ),
                    dmc.TextInput(
                        id="signup-submit-cpf",
                        type="text",
                        label="CPF (somente números)",
                        placeholder="12345678901",
                        required=True,
                    ),
                    dmc.TextInput(
                        id="signup-submit-email",
                        type="email",
                        label="Email",
                        placeholder="fulano.silva@gmail.com",
                        required=True,
                    ),
                    dmc.PasswordInput(
                        id="signup-submit-senha",
                        label="Senha",
                        placeholder="#MinhaSenhaForte42",
                        required=True,
                    ),
                    dmc.PasswordInput(
                        id="signup-submit-senha-check",
                        label="Confirme a senha",
                        placeholder="#MinhaSenhaForte42",
                        required=True,
                    ),
                    dmc.Button(
                        "Criar conta",
                        id="signup-btn",
                        fullWidth=True,
                        mt="1rem",
                        variant="solid",
                    ),
                    dmc.Group(
                        [
                            dmc.Text("Já tem uma conta?", size=12),
                            dmc.Anchor("Faça login", href="/login", size=12),
                        ],
                        spacing=5,
                        position="center",
                        mt="0.5rem",
                    ),
                    html.Div(id="signup-feedback"),
                ]
            )
        ],
        w=350,
        p="1rem",
    )
]


def layout():
    if not current_user.is_authenticated:
        return signup_card
    else:
        return already_logged_layout


@callback(
    Output("signup-feedback", "children"),
    State("signup-submit-nome", "value"),
    State("signup-submit-sobrenome", "value"),
    State("signup-submit-cpf", "value"),
    State("signup-submit-email", "value"),
    State("signup-submit-senha", "value"),
    State("signup-submit-senha-check", "value"),
    Input("signup-btn", "n_clicks"),
    prevent_initial_call=True,
)
def signup_new_user(nome, sobrenome, cpf, email, senha, senha2, n):
    if not n:
        raise PreventUpdate
    try:
        novo_usuario = NovoUsuario(
            nome=nome,
            sobrenome=sobrenome,
            cpf=cpf,
            email=email,
            senha=senha,
            senha_check=senha2,
        )
        status_registro = novo_usuario.registrar()
    except ValidationError as e:
        erro = e.errors()[0]["ctx"]["error"]
        print(erro)
        return [dmc.Alert(str(erro), color="red", variant="filled")]
    except AssertionError as e:
        return [dmc.Alert(str(e), color="red", variant="filled")]

    if status_registro:
        return [dmc.Alert("Registrado com sucesso", color="green", variant="filled")]
    else:
        return [dmc.Alert("Email já cadastrado", color="red", variant="filled")]
