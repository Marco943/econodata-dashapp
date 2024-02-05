import dash_mantine_components as dmc
from dash import Input, Output, State, callback, register_page
from dash.exceptions import PreventUpdate
from flask_mail import Message
from utils.models import mail

register_page(__name__, path="/user/configuracoes", title="Configurações")


def layout():
    return dmc.Container(
        [
            dmc.TextInput(type="email", id="cfg-email-adr"),
            dmc.Textarea(id="cfg-text-area"),
            dmc.Button("Enviar e-mail", id="cfg-enviar-email-btn"),
        ]
    )


@callback(
    Output("cfg-text-area", "children"),
    Input("cfg-enviar-email-btn", "n_clicks"),
    State("cfg-email-adr", "children"),
    State("cfg-text-area", "children"),
    prevent_initial_call=True,
)
def enviar_email(n, email, texto):
    if not n:
        raise PreventUpdate
    msg = Message(
        "Olá",
        body=texto,
        sender="macto.14@gmail.com",
        recipients=[email],
    )
    mail.send(msg)
    raise PreventUpdate
