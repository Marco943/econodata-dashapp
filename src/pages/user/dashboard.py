from datetime import datetime
from pathlib import Path

import dash_mantine_components as dmc
import orjson
import plotly.graph_objects as go
from components.no_permission import no_permission_layout
from dash import (
    Input,
    Output,
    State,
    _configs,
    callback,
    dcc,
    get_asset_url,
    register_page,
)
from dash.exceptions import PreventUpdate
from flask_login import current_user
from utils.dados import CONFIGS_PLOTLY, TEMPLATE_PLOTLY, baixar_dados_bcb

register_page(__name__, path="/user/dashboard", title="Dashboard")


def layout():
    if not current_user.is_authenticated:
        return no_permission_layout
    with open("src/assets/metadados.json", "rb") as f:
        metadados_bcb = [
            {"value": indicador["c"], "label": f"{indicador['n']} ({indicador['f']})"}
            for indicador in orjson.loads(f.read())
        ]

    indicadores = [baixar_dados_bcb(1207, datetime(2000, 1, 1), datetime(2023, 1, 1))]

    fig = go.Figure(
        data=[
            go.Scatter(
                name=indicador,
                x=dados.get_column("d"),
                y=dados.get_column("v"),
                mode="lines+markers",
            )
            for indicador, dados in indicadores
        ],
        layout=go.Layout(template=TEMPLATE_PLOTLY),
    )

    return dmc.Container(
        fluid=True,
        children=[
            dmc.Title(children="Dashboard", order=1, weight=500, mb="1rem"),
            dmc.Select(
                id="select-indicadores-dash",
                label="Indicador",
                data=metadados_bcb,
                placeholder="Selecione um indicador",
            ),
            dmc.DateRangePicker(
                id="dt-range-dash",
                label="Selecione o período",
                initialLevel="month",
                allowLevelChange=False,
                locale="pt-br",
            ),
            dmc.Button(id="btn-gerar-grafico-dash", children="Gerar gráfico"),
            dcc.Graph(figure=fig, animate=True, config=CONFIGS_PLOTLY),
        ],
    )
