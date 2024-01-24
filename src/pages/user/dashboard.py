import dash_mantine_components as dmc
from components.no_permission import no_permission_layout
from dash import html, register_page
from flask_login import current_user

register_page(__name__, path="/user/dashboard", title="Dashboard")


def layout():
    if not current_user.is_authenticated:
        return no_permission_layout
    else:
        return html.Div(
            [
                html.Div([dmc.Text("Dashboard")], className="content"),
            ]
        )
