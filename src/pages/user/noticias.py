from math import ceil

import dash_mantine_components as dmc
from dash import Input, Output, callback, html, register_page
from utils.models import mongo

register_page(__name__, path="/user/noticias", title="Notícias")

BATELADA_NOTICIAS = 5


def caixa_noticia(noticia: dict):
    return dmc.Card(
        [
            dmc.CardSection(
                dmc.Grid(
                    [
                        dmc.Col(
                            dmc.Image(
                                src=noticia.get("img", None),
                                width=150,
                                height=80,
                                withPlaceholder=True,
                                display="block",
                            ),
                            span="content",
                            p=0,
                        ),
                        dmc.Col(
                            dmc.Anchor(
                                dmc.Text(noticia["mat"], size="lg"),
                                href=noticia["url"],
                            ),
                            span="auto",
                        ),
                    ],
                    m=0,
                ),
                withBorder=True,
            ),
            dmc.CardSection(
                dmc.Text(
                    [
                        noticia["f"].upper(),
                        " - ",
                        noticia["dt"].strftime("%d/%m/%Y %H:%M"),
                    ],
                    size="xs",
                    italic=True,
                    color="dimmed",
                ),
                px="0.5rem",
            ),
        ],
        radius="md",
        withBorder=True,
        mb="1rem",
    )


def layout():
    total_noticias = ceil(mongo.db["Notícias"].count_documents({}) / BATELADA_NOTICIAS)
    return dmc.Container(
        [
            html.Div(id="noticias-corpo"),
            dmc.Pagination(total=total_noticias, id="noticias-nav", page=1),
        ]
    )


@callback(
    Output("noticias-corpo", "children"),
    Input("noticias-nav", "page"),
)
def mudar_pagina_noticias(pag: int):
    noticias = mongo.db["Notícias"].aggregate(
        [
            {"$sort": {"dt": -1}},
            {"$skip": BATELADA_NOTICIAS * (pag - 1)},
            {"$limit": BATELADA_NOTICIAS},
        ]
    )
    return [caixa_noticia(noticia) for noticia in noticias]
