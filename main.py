# SCRIPT PRINCIPAL
# Este script es el que se encarga de "enrutar" o "configurar" como se
# ejecutan las páginas. Para agregar una página, simplemente agrega un
# elif debajo y la ruta de la misma.

import flet as ft
import asyncio

from src.ui.pages.main_page import view as main_view
from src.ui.pages.newton_cooling_law_page import view as ncl_view
from src.ui.constants.theme_colors import DARK_COLORS


async def main(page: ft.Page):

    def route_change():
        page.views.clear()

        ## PÁGINA DE DEBUG
        page.views.append(
            # Este view es solo un placeholder para poder acceder a todas las páginas.
            ft.View(
                route="/",
                controls=[
                    ft.Text(
                        "AQUÍ VA LA PÁGINA PRINCIPAL ):", color=DARK_COLORS["text"]
                    ),
                    ft.ElevatedButton(
                        "Ir a Página Principal",
                        on_click=lambda _: asyncio.create_task(
                            page.push_route("/main_page")
                        ),
                    ),
                    ft.ElevatedButton(
                        "Ir a NCL",
                        on_click=lambda _: asyncio.create_task(page.push_route("/ncl")),
                    ),
                ],
                appbar=ft.AppBar(
                    title=ft.Text("Página Principal"), bgcolor=DARK_COLORS["cold"]
                ),
            )
        )

        ## PÁGINA PRINCIPAL
        if page.route == "/main_page":
            page.views.append(main_view(page))

        ## PÁGINA DEL NCL
        if page.route == "/ncl":
            page.views.append(ncl_view(page))

        page.update()

    page.on_route_change = route_change
    route_change()


ft.run(main)
