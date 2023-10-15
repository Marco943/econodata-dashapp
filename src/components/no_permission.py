import dash_mantine_components as dmc

no_permission_layout = [
    dmc.Title("Você não tem permissão para visualizar esta página", order=1),
    dmc.Group(
        [
            dmc.Anchor("Conecte-se", href="/login"),
            dmc.Text("ou"),
            dmc.Anchor("Crie uma conta", href="/signup"),
        ],
        spacing=5,
        mt="1rem",
    ),
]
