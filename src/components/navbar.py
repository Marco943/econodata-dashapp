import dash_mantine_components as dmc
from components.header import ALTURA_HEADER

LARGURA_NAVBAR = 200

navbar_layout = dmc.Navbar(
    [dmc.Text("Barra de navegação")],
    fixed=True,
    width={"base": LARGURA_NAVBAR},
    position={"top": ALTURA_HEADER},
)
