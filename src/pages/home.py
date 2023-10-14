from dash import Dash, html, dcc, callback, callback_context, register_page
import dash_mantine_components as dmc
from flask_login import current_user

register_page(__name__, path="/", title="Início")


def layout():
    if not current_user.is_authenticated:
        return [
            dmc.Text("Você não tem permissão para visualizar esta página"),
            dmc.Group(
                [
                    dmc.Anchor("Conecte-se", href="/login"),
                    dmc.Text("ou"),
                    dmc.Anchor("Crie uma conta", href="/register"),
                ],
                spacing=2,
            ),
        ]

    else:
        return [dmc.Text(f"Seja bem-vindo, {current_user.username}")]
