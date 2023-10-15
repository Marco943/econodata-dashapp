from dash import register_page, Output, Input, State, callback, html
from dash.exceptions import PreventUpdate
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from utils.models import User
from utils.validacoes import validar_email, validar_senha, validar_cpf

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

layout = signup_card


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
    elif not (nome or sobrenome or cpf or email or senha or senha2):
        return [dmc.Alert("Preencha todos os campos", color="red", variant="filled")]
    elif not validar_email(email):
        return [dmc.Alert("Email inválido", color="red", variant="filled")]
    elif not validar_cpf(cpf):
        return [dmc.Alert("CPF inválido", color="red", variant="filled")]
    elif not validar_senha(senha):
        return [dmc.Alert("Senha fraca", color="red", variant="filled")]
    elif not senha == senha2:
        return [dmc.Alert("As senhas não são iguais", color="red", variant="filled")]
    else:
        new_user = User(None, nome, sobrenome, cpf, email, senha)
        status_signup = new_user.signup()
        if status_signup:
            return [
                dmc.Alert("Registrado com sucesso", color="green", variant="filled")
            ]
        else:
            return [dmc.Alert("Email já cadastrado", color="red", variant="filled")]
