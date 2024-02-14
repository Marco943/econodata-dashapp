import dash_mantine_components as dmc
from components.no_permission import no_permission_layout
from dash import Dash, callback, callback_context, dcc, html, register_page
from flask_login import current_user

register_page(__name__, path="/", title="Início")


def layout(next=None):
    if current_user.is_authenticated:
        sub_layout = [
            dmc.Title(f"Olá, {current_user.nome}", order=1),
            dmc.Group(
                [
                    dmc.Anchor(
                        "Acesse o Dashboard", href="/user/dashboard/macroeconomia"
                    ),
                ],
                spacing=5,
                mt="1rem",
            ),
        ]
    else:
        sub_layout = no_permission_layout
    return html.Div(
        [
            dmc.Title("Lorem ipsum", order=1),
            dmc.Text(
                "Dolor sit amet, consectetur adipiscing elit. Sed tincidunt quis ligula ac dapibus. Ut finibus risus ut orci convallis, eget porttitor magna tincidunt. Morbi pretium metus at quam scelerisque, vel vestibulum nisi finibus. Pellentesque porta viverra odio ac condimentum. Maecenas sit amet facilisis nisi. In hac habitasse platea dictumst. In gravida, nisi nec luctus ultrices, orci lacus sagittis nisi, ut mollis diam purus non justo. Nulla justo tellus, vulputate sed viverra sollicitudin, auctor ac nisl. Phasellus at purus lobortis, scelerisque lectus vitae, consectetur orci. Nullam nec egestas ligula. "
            ),
            *sub_layout,
        ],
    )
