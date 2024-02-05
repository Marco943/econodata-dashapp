from math import ceil

import dash_mantine_components as dmc
from dash import Input, Output, callback, html, register_page
from utils.models import mongo

register_page(__name__, path="/user/noticias", title="Notícias")

BATELADA_NOTICIAS = 5


def caixa_noticia(noticia: dict):
    return dmc.Anchor(
        href=noticia["url"],
        underline=False,
        target="_blank",
        children=dmc.Card(
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
                                dmc.Text(noticia["mat"], size="lg"),
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
        ),
    )


def layout():
    total_noticias = ceil(mongo.db["Notícias"].count_documents({}) / BATELADA_NOTICIAS)
    return dmc.Container(
        [
            dmc.Title("Notícias", order=1, weight=500, mb="1rem"),
            dmc.Skeleton(
                height=572,
                visible=False,
                width="100%",
                children=html.Div(id="noticias-corpo", style={"width": "100%"}),
                mb="1rem",
            ),
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
