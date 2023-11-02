from dash import Dash, html, dcc, callback, callback_context, register_page
import dash_mantine_components as dmc
from flask_login import current_user
from components.no_permission import no_permission_layout
from components.header import header_layout
from components.navbar import navbar_layout, drawer_navbar_layout

register_page(__name__, path="/user/dashboard", title="Dashboard")


def layout():
    if not current_user.is_authenticated:
        return no_permission_layout
    else:
        return html.Div(
            [
                header_layout(),
                navbar_layout(),
                drawer_navbar_layout(),
                html.Div([dmc.Text("Dashboard")], className="content"),
            ]
        )
