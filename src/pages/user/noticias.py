from math import ceil

import dash_mantine_components as dmc
from dash import Input, Output, callback, html, register_page
from utils.models import mongo

register_page(__name__, path="/user/noticias", title="Notícias")

BATELADA_NOTICIAS = 5


def caixa_noticia(noticia: dict):
    return dmc.Paper(
        h=80,
        mb="1rem",
        withBorder=True,
        children=dmc.Anchor(
            href=noticia["url"],
            underline=False,
            target="_blank",
            children=dmc.Grid(
                m=0,
                h=80,
                children=[
                    dmc.Col(
                        span="content",
                        bg="yellow",
                        c="white",
                        children=[
                            dmc.Text(
                                children=noticia["dt"].strftime("%d %b"),
                                weight=100,
                                size="lg",
                            ),
                            dmc.Text(
                                children=noticia["dt"].strftime("%H:%M"),
                                weight=600,
                                size="lg",
                            ),
                        ],
                    ),
                    dmc.Col(
                        span="content",
                        p=0,
                        children=dmc.Image(
                            src=noticia.get("img", None),
                            width=150,
                            height=80,
                            withPlaceholder=True,
                            display="block",
                        ),
                    ),
                    dmc.Col(
                        span="auto",
                        children=dmc.Text(
                            children=[
                                dmc.Anchor(
                                    children=noticia["mat"],
                                    href=noticia["url"],
                                    size="lg",
                                    weight=600,
                                ),
                                dmc.Text(
                                    children=f'Fonte: {noticia["f"]}',
                                    color="dimmed",
                                    italic=True,
                                    size="xs",
                                ),
                            ],
                        ),
                    ),
                ],
            ),
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
                mb="1rem",
                children=html.Div(id="noticias-corpo", style={"width": "100%"}),
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
