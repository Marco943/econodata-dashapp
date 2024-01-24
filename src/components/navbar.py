import dash_mantine_components as dmc
from components.header import ALTURA_HEADER
from dash_iconify import DashIconify
from flask_login import current_user

LARGURA_NAVBAR = 200


def navbar_content():
    if not current_user.is_authenticated:
        return dmc.Center(
            dmc.Stack(
                [
                    dmc.Text("Você não está logado"),
                    dmc.Button("Faça Login"),
                    dmc.Text("ou", align="center"),
                    dmc.Button("Crie uma conta", variant="outline"),
                ],
                spacing="xs",
            ),
            style={"height": "100%", "width": "100%"},
        )
    return [
        dmc.AccordionMultiple(
            [
                dmc.AccordionItem(
                    [
                        dmc.AccordionControl(
                            "Dashboard",
                            icon=DashIconify(icon="heroicons:home-20-solid"),
                        ),
                        dmc.AccordionPanel(
                            [
                                dmc.NavLink(label="Mercado"),
                                dmc.NavLink(label="Macroeconomia"),
                                dmc.NavLink(label="Setor Externo"),
                                dmc.NavLink(label="Analises"),
                                dmc.NavLink(label="Visão Geral"),
                            ],
                            p=0,
                        ),
                    ],
                    value="dashboard",
                ),
                dmc.AccordionItem(
                    [
                        dmc.AccordionControl(
                            "Posts", icon=DashIconify(icon="solar:document-bold")
                        ),
                        dmc.AccordionPanel(
                            [
                                dmc.NavLink(label="Notícias"),
                                dmc.NavLink(label="Categorias"),
                            ]
                        ),
                    ],
                    value="posts",
                ),
            ],
        ),
    ]


def navbar_layout():
    return dmc.MediaQuery(
        dmc.Navbar(
            navbar_content(),
            fixed=True,
            width={"base": LARGURA_NAVBAR},
            position={"top": ALTURA_HEADER},
            id="side-navbar",
            pl=0,
        ),
        smallerThan=1201,
        styles={"display": "none"},
    )


def drawer_navbar_layout():
    return dmc.Drawer(
        navbar_content(),
        id="drawer-navbar",
        opened=False,
        zIndex=100000,
        size=300,
        transitionDuration=100,
    )
