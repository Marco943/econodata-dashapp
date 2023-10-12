from dash import Dash, html, dcc, callback, callback_context, register_page
import dash_mantine_components as dmc
from dash_iconify import DashIconify

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
                dmc.Button(
                    "Conectar-se",
                    id="login-btn",
                    fullWidth=True,
                    mt="1rem",
                    variant="solid",
                ),
                dmc.Group(
                    [
                        dmc.Text("Não tem conta?", size=12),
                        dmc.Anchor("Crie uma", href="/register", size=12),
                    ],
                    spacing=2,
                    position="center",
                    mt="0.5rem",
                ),
            ]
        )
    ],
    p="1rem",
    w=350,
)

layout = html.Div(
    [
        dmc.Title("Bem-vindo!", order=1),
        dmc.Text("Entre na sua conta para continuar", size="sm"),
        login_card,
    ]
)
