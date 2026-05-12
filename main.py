# SCRIPT PRINCIPAL
# Este script es el que se encarga de "enrutar" o "configurar" como se
# ejecutan las páginas. Para agregar una página, simplemente agrega un
# elif debajo y la ruta de la misma.

import flet as ft

from src.ui.pages.main_page import view as main_view
from src.ui.pages.newton_cooling_law_page import view as ncl_view
from src.ui.constants.theme_colors import DARK_COLORS


async def main(page: ft.Page):

    def route_change():
        page.views.clear()

        page.views.append(ft.View(route="/", controls=[]))

        ## PÁGINA PRINCIPAL
        page.views.append(main_view(page))

        ## PÁGINA DEL NCL
        if page.route == "/ncl":
            page.views.append(ncl_view(page))

        page.update()

    page.on_route_change = route_change
    route_change()


ft.run(main)
