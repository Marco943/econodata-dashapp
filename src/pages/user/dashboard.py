from dash import Dash, html, dcc, callback, callback_context, register_page
import dash_mantine_components as dmc
from flask_login import current_user
from components.no_permission import no_permission_layout

register_page(__name__, path="/dashboard", title="Dashboard")


def layout():
    return dmc.Text("oi")
