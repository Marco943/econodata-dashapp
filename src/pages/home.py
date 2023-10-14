from dash import Dash, html, dcc, callback, callback_context, register_page
import dash_mantine_components as dmc
from flask_login import current_user
from components.no_permission import no_permission_layout

register_page(__name__, path="/", title="Início")


def layout():
    if not current_user.is_authenticated:
        return no_permission_layout

    else:
        return [dmc.Text(f"Seja bem-vindo, {current_user.username}")]
