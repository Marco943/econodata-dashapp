import dash_mantine_components as dmc
from dash import callback, Output, Input, Patch, html, clientside_callback, State
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify
from flask_login import current_user, logout_user
from icecream import ic

ALTURA_HEADER = 60


def build_user_header():
    if current_user.is_authenticated:
        user_status_layout = dmc.Menu(
            [
                dmc.MenuTarget(
                    dmc.Button(
                        current_user.nome,
                        variant="light",
                        rightIcon=DashIconify(icon="bxs:down-arrow"),
                    )
                ),
                dmc.MenuDropdown(
                    [
                        dmc.MenuItem(
                            "Configurações",
                            icon=DashIconify(icon="solar:settings-bold"),
                        ),
                        dmc.MenuDivider(),
                        dmc.MenuItem(
                            "Sair",
                            id="logout-header-btn",
                            icon=DashIconify(icon="bxs:exit"),
                        ),
                    ]
                ),
            ]
        )
    else:
        user_status_layout = dmc.Button("Login", id="btn-goto-login")
    return user_status_layout


header_layout = dmc.Header(
    dmc.Stack(
        [
            dmc.Grid(
                [
                    dmc.MediaQuery(
                        dmc.Col(
                            dmc.ActionIcon(
                                DashIconify(icon="radix-icons:hamburger-menu"),
                                id="btn-hamburger",
                            ),
                            id="col-hamburger",
                            span="auto",
                        ),
                        largerThan=1201,
                        styles={"display": "none"},
                    ),
                    dmc.Col(
                        dmc.Title("Econ", color="yellow", order=2), span="content", pr=0
                    ),
                    dmc.Col(dmc.Title("odata", order=2), span="auto", pl=0),
                    dmc.Col(
                        dmc.Group(
                            [
                                html.Div(id="component-user-header"),
                                dmc.Switch(
                                    offLabel=DashIconify(
                                        icon="radix-icons:moon", width=20
                                    ),
                                    onLabel=DashIconify(
                                        icon="radix-icons:sun", width=20
                                    ),
                                    id="switch-theme",
                                    checked=True,
                                    size="md",
                                ),
                            ]
                        ),
                        span="content",
                    ),
                ],
                justify="space-between",
                align="center",
                style={"height": ALTURA_HEADER, "margin": 0},
            )
        ],
        justify="space-between",
        style={"height": ALTURA_HEADER},
    ),
    height=ALTURA_HEADER,
    fixed=True,
)

clientside_callback(
    """function(n_clicks) { return true }""",
    Output("drawer-navbar", "opened"),
    Input("btn-hamburger", "n_clicks"),
    prevent_initial_call=True,
)

clientside_callback(
    """ function(data) { return data } """,
    Output("mantine-main-provider", "theme"),
    Input("theme-store", "data"),
)

clientside_callback(
    """function(checked, data) {
        if (data) {
            var primarycolor = data["primaryColor"];
            if (checked) {
                return { colorScheme: "light", primaryColor: primarycolor }
            } else {
                return {colorScheme: "dark", primaryColor: primarycolor }
            }
        } else {
            return { colorScheme: "light", primaryColor: "yellow" }
        }
    }""",
    Output("theme-store", "data"),
    Input("switch-theme", "checked"),
    State("theme-store", "data"),
)


@callback(
    Output("url", "pathname", allow_duplicate=True),
    Input("btn-goto-login", "n_clicks"),
    prevent_initial_call=True,
)
def redirecionar(n_clicks):
    if n_clicks:
        return "/login"
    else:
        raise PreventUpdate


@callback(Output("component-user-header", "children"), Input("url", "pathname"))
def update_user_header(url):
    return build_user_header()


@callback(
    Output("url", "pathname", allow_duplicate=True),
    Input("logout-header-btn", "n_clicks"),
    prevent_initial_call=True,
)
def logout(n_clicks):
    if n_clicks:
        logout_user()
        return "/login"
    else:
        raise PreventUpdate
