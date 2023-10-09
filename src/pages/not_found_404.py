from dash import Dash, html, dcc, callback, callback_context, register_page
import dash_mantine_components as dmc
from dash_iconify import DashIconify

register_page(__name__)

layout = [
    dmc.Stack(
        [
            dmc.Title("Essa página não existe", order=1),
            dmc.Anchor("Voltar à pagina inicial", href="/", mt="1rem"),
        ],
        align="left",
        justify="center",
        style={"height": "50vh"},
    )
]
