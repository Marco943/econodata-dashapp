from datetime import datetime

import orjson
import plotly.graph_objects as go
import polars as pl
from utils.models import cache, mongo

with open("src/assets/metadados.json", "rb") as f:
    METADADOS_BCB = orjson.loads(f.read())


@cache.memoize()
def mongo_dados_bcb(
    codigo: int, data_inicial: datetime, data_final: datetime
) -> tuple[str, pl.DataFrame]:
    dados = pl.DataFrame(
        mongo.cx["Econodata"]["Dados"].find(
            {"c": codigo, "d": {"$gte": data_inicial, "$lte": data_final}},
            {"_id": 0, "d": 1, "v": 1},
        )
    )
    nome = [metadado["n"] for metadado in METADADOS_BCB if metadado["c"] == codigo][0]
    return nome, dados


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
        plot_bgcolor="#fff",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=go.layout.XAxis(
            gridcolor="#f3f3f3",
            minor=go.layout.xaxis.Minor(gridcolor="#f3f3f3"),
            zerolinecolor="#bbb",
            zerolinewidth=2,
            titlefont=go.layout.xaxis.title.Font(color="#000"),
            tickfont=go.layout.xaxis.Tickfont(color="gray"),
        ),
        yaxis=go.layout.YAxis(
            gridcolor="#f3f3f3",
            minor=go.layout.yaxis.Minor(gridcolor="#f3f3f3"),
            zerolinecolor="#bbb",
            zerolinewidth=2,
            titlefont=go.layout.yaxis.title.Font(color="#000"),
            tickfont=go.layout.yaxis.Tickfont(color="gray"),
        ),
        margin=go.layout.Margin(autoexpand=True, l=60, r=40),
        legend=go.layout.Legend(
            title=go.layout.legend.Title(
                font=go.layout.legend.title.Font(color="gray", size=12)
            ),
            orientation="h",
            y=1,
            x=0.5,
            yanchor="bottom",
            xanchor="center",
        ),
        hovermode="x unified",
        hoverlabel=go.layout.Hoverlabel(
            bgcolor="#fff",
            bordercolor="#ffe066",
            font=go.layout.hoverlabel.Font(color="#000"),
        ),
    )
)
