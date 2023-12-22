import dash_mantine_components as dmc
from dash import Dash, dcc, html, page_container

app = Dash(
    use_pages=True,
    suppress_callback_exceptions=True,
    title="App Econodata",
    update_title=None,
    server=False,
    prevent_initial_callbacks=True,
)


app.layout = dmc.MantineProvider(
    [
        dcc.Store(id="theme-store", storage_type="local"),
        dcc.Location(id="url", refresh=True),
        dmc.NotificationsProvider(
            [
                html.Div(
                    dmc.Container(
                        page_container,
                        fluid=True,
                        px=0,
                    ),
                    style={"height": "100vh"},
                )
            ]
        ),
    ],
    theme={"colorScheme": "light", "primaryColor": "yellow"},
    id="mantine-main-provider",
    inherit=True,
    withGlobalStyles=True,
    withNormalizeCSS=True,
)
