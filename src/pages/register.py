from dash import callback, register_page, Input, Output, State
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from werkzeug.security import generate_password_hash

register_page(__name__, path="/register", title="Criar uma conta")

register_card = [
    dmc.Card(
        [
            dmc.CardSection(
                [
                    dmc.Title("Criar uma conta", order=4, ta="center"),
                    dmc.TextInput(
                        id="register-in-user",
                        type="text",
                        label="Nome de usuário",
                        icon=DashIconify(icon="ant-design:user-outlined"),
                    ),
                    dmc.TextInput(
                        id="register-in-email",
                        type="email",
                        label="Email",
                        icon=DashIconify(icon="ic:round-alternate-email"),
                    ),
                    dmc.PasswordInput(
                        id="register-in-pwd",
                        label="Senha",
                        icon=DashIconify(icon="carbon:password"),
                    ),
                    dmc.PasswordInput(
                        id="register-in-pwd2",
                        label="Confirme a senha",
                        icon=DashIconify(icon="carbon:password"),
                    ),
                    dmc.Button(
                        "Criar",
                        id="register-btn",
                        fullWidth=True,
                        mt="1rem",
                        variant="gradient",
                    ),
                    dmc.Group(
                        [
                            dmc.Text("Já tem uma conta?", size=12),
                            dmc.Anchor("Faça login", href="/login", size=12),
                        ],
                        spacing=2,
                        position="center",
                        mt="0.5rem",
                    ),
                    dmc.Text(id="register-info"),
                ]
            )
        ],
        w=350,
        p="1rem",
        shadow="sm",
        radius="md",
    )
]

layout = register_card
