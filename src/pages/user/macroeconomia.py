from datetime import datetime

import dash_mantine_components as dmc
import plotly.graph_objects as go
from components.no_permission import no_permission_layout
from dash import Input, Output, Patch, State, callback, dcc, register_page
from dash.exceptions import PreventUpdate
from flask_login import current_user
from utils.dados import CONFIGS_PLOTLY, METADADOS_BCB, TEMPLATE_PLOTLY, mongo_dados_bcb

register_page(__name__, path="/user/dashboard/macroeconomia", title="Dashboard")


def layout():
    if not current_user.is_authenticated:
        return no_permission_layout

    return dmc.Container(
        fluid=True,
        children=[
            dmc.Title(children="Dashboard", order=1, weight=500, mb="1rem"),
            dmc.Grid(
                children=[
                    dmc.Col(
                        span="auto",
                        children=dmc.MultiSelect(
                            id="select-indicadores-dash",
                            label="Indicador",
                            clearable=True,
                            data=[
                                {
                                    "value": indicador["c"],
                                    "label": f"{indicador['n']} ({indicador['f']})",
                                }
                                for indicador in METADADOS_BCB
                            ],
                            placeholder="Selecione um indicador",
                        ),
                    ),
                    dmc.Col(
                        span="content",
                        children=dmc.Button(
                            id="btn-gerar-grafico-dash", children="Gerar gráfico"
                        ),
                    ),
                ],
                align="end",
            ),
            dcc.Graph(
                figure=go.Figure(layout=go.Layout(template=TEMPLATE_PLOTLY)),
                id="graph-grafico-dash",
                config=CONFIGS_PLOTLY,
            ),
        ],
    )


@callback(
    Output("graph-grafico-dash", "figure"),
    Input("btn-gerar-grafico-dash", "n_clicks"),
    State("select-indicadores-dash", "value"),
    State("theme-store", "data"),
)
def gerar_grafico_indicadores_macro(n, cod_indicadores: list[int], tema):
    if not n:
        raise PreventUpdate

    indicadores = [
        mongo_dados_bcb(cod, datetime(2000, 1, 1), datetime(2023, 1, 1))
        for cod in cod_indicadores
    ]

    patch_figure = Patch()
    patch_figure["data"] = []

    for i, (indicador, dados) in enumerate(indicadores):
        patch_figure["data"][i] = {
            "x": dados.get_column("d").to_list(),
            "y": dados.get_column("v").to_list(),
            "name": indicador,
            "mode": "lines+markers",
        }
    return patch_figure
