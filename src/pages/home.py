from dash import Dash, html, dcc, callback, callback_context, register_page
import dash_mantine_components as dmc

register_page(__name__, path="/", title="Início")

layout = dmc.Text("Início")
