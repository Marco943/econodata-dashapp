from dash import Dash, html, dcc, callback, callback_context, register_page
import dash_mantine_components as dmc
from flask_login import current_user
from components.no_permission import no_permission_layout

register_page(__name__, path="/", title="Início")


def layout(next=None):
    return html.Div(
        [
            dmc.Title("Lorem ipsum", order=1),
            dmc.Text(
                "Dolor sit amet, consectetur adipiscing elit. Sed tincidunt quis ligula ac dapibus. Ut finibus risus ut orci convallis, eget porttitor magna tincidunt. Morbi pretium metus at quam scelerisque, vel vestibulum nisi finibus. Pellentesque porta viverra odio ac condimentum. Maecenas sit amet facilisis nisi. In hac habitasse platea dictumst. In gravida, nisi nec luctus ultrices, orci lacus sagittis nisi, ut mollis diam purus non justo. Nulla justo tellus, vulputate sed viverra sollicitudin, auctor ac nisl. Phasellus at purus lobortis, scelerisque lectus vitae, consectetur orci. Nullam nec egestas ligula. "
            ),
            *no_permission_layout,
        ],
    )
