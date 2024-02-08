from datetime import datetime

import plotly.graph_objects as go
import polars as pl
from utils.models import mongo


def baixar_dados_bcb(
    codigo: int, data_inicial: datetime, data_final: datetime
) -> tuple[str, pl.DataFrame]:
    dados = pl.DataFrame(
        mongo.cx["Econodata"]["Dados"].find(
            {"c": codigo, "d": {"$gte": data_inicial, "$lte": data_final}},
            {"_id": 0, "d": 1, "v": 1},
        )
    )
    return "_nome_indicador_", dados


CONFIGS_PLOTLY = {"displayModeBar": False, "displaylogo": False, "locale": "pt-BR"}

TEMPLATE_PLOTLY = go.layout.Template(
    layout=go.Layout(
        title=go.layout.Title(
            x=0, xanchor="left", xref="paper", font=go.layout.title.Font()
        ),
        separators=",.",
        font=go.layout.Font(
            family="BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif, Apple Color Emoji, Segoe UI Emoji"
        ),
        plot_bgcolor="#ededed",
        xaxis=go.layout.XAxis(
            gridcolor="#FFF",
            minor=go.layout.xaxis.Minor(gridcolor="#FFF"),
            zerolinecolor="#FFF",
            zerolinewidth=2,
            titlefont=go.layout.xaxis.title.Font(color="#000"),
            tickfont=go.layout.xaxis.Tickfont(color="gray"),
        ),
        yaxis=go.layout.YAxis(
            gridcolor="#FFF",
            minor=go.layout.yaxis.Minor(gridcolor="#FFF"),
            zerolinecolor="#FFF",
            zerolinewidth=2,
            titlefont=go.layout.yaxis.title.Font(color="#000"),
            tickfont=go.layout.yaxis.Tickfont(color="gray"),
        ),
        margin=go.layout.Margin(autoexpand=True, l=60, r=40),
        legend=go.layout.Legend(
            title=go.layout.legend.Title(
                font=go.layout.legend.title.Font(color="gray", size=12)
            )
        ),
        hovermode="x",
        hoverlabel=go.layout.Hoverlabel(
            bgcolor="#fff",
            bordercolor="#ffe066",
            font=go.layout.hoverlabel.Font(color="#000"),
        ),
    )
)
