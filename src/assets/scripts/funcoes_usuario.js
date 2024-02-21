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
            if (!data) {
                data = { colorScheme: "light", primaryColor: "yellow" }
            }
            if (n_clicks) {
                data.colorScheme = data.colorScheme == "dark" ? "light" : "dark"
            }

            // this.trocar_tema_plotly(data.colorScheme);
            return data
        },
        atualizar_pagina: function (_) {
            location.reload();
            throw window.dash_clientside.PreventUpdate;
        },

        // trocar_tema_plotly: function (colorScheme) {
        //     document.querySelectorAll('.js-plotly-plot').forEach(
        //         function (gd) {
        //             Plotly.relayout(gd, {
        //                 "template.layout.title.text": colorScheme
        //             })
        //         }
        //     )
        // }
    }
});