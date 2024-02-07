from datetime import datetime

import dash_mantine_components as dmc
import plotly.graph_objects as go
import polars as pl
from components.no_permission import no_permission_layout
from dash import dcc, html, register_page
from flask_login import current_user
from utils.models import graph_configs, mongo

register_page(__name__, path="/user/dashboard", title="Dashboard")


def layout():
    if not current_user.is_authenticated:
        return no_permission_layout

    dados = pl.DataFrame(
        mongo.cx["Econodata"]["Dados"].find(
            {"c": 1207, "d": {"$gt": datetime(2000, 1, 1)}}, {"_id": 0, "d": 1, "v": 1}
        )
    )
    fig = go.Figure(
        data=[
            go.Scatter(
                x=dados.get_column("d"), y=dados.get_column("v"), mode="lines+markers"
            )
        ]
    )

    return dmc.Container(
        fluid=True,
        children=[
            dmc.Title("Dashboard", order=1, weight=500, mb="1rem"),
            dcc.Graph(figure=fig, animate=True, config=graph_configs),
        ],
    )
