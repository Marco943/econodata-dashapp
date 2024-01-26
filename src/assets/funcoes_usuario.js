window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        carregar_tema_cache: function (data) {
            if (data) {
                return data
            } else {
                return { colorScheme: scheme, primaryColor: "yellow" }
            }
        },

        abrir_hamburger_menu: function (n_clicks) { return true },

        trocar_tema: function (n_clicks, data) {
            if (data) {
                if (n_clicks) {
                    data.colorScheme = data.colorScheme == "dark" ? "light" : "dark"
                    return data
                } else {
                    throw window.dash_clientside.PreventUpdate
                }
            }
            return { colorScheme: "light", primaryColor: "yellow" }

        }
    }
});