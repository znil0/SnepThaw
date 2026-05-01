# PÁGINA: Ley de Enfriamiento de Newton (PLAN A) -Versión 2-
# En esta página el usuario puede ingresar las mediciones de temperatura y
# revisar la información y gráficos generados a partir de estas.
# NOTA: Solo es válido para líquidos muy conductores como el agua.

import flet as ft
import asyncio

from src.ui.constants.theme_colors import LIGHT_COLORS
from src.ui.constants.text_styles import TEXT_STYLES


# BLOQUE DE DESCRIPCIÓN ________________________________________________________
# Contiene el título y la descripción que se muestra en la parte superior
# de la página.

title_block_style: dict = {
    "expand": True,
    "padding": 30,
    "bgcolor": ft.Colors.WHITE,
    "border_radius": ft.BorderRadius(
        top_left=0,  # esquina superior izquierda sin redondear
        top_right=0,  # esquina superior derecha sin redondear
        bottom_left=20,  # esquina inferior izquierda redondeada
        bottom_right=20,  # esquina inferior derecha redondeada
    ),
}


class TitleBlock(ft.Container):
    def __init__(self):
        super().__init__(**title_block_style)

        breadcrumbs = ft.Row(
            expand_loose=True,
            spacing=0,
            controls=[
                ft.Text("SnepThaw", **TEXT_STYLES["breadcrumb_secondary_style"]),
                ft.Icon(
                    width=30,
                    height=30,
                    icon=ft.Icons.CHEVRON_RIGHT,
                    color=LIGHT_COLORS["secondary"],
                ),
                ft.Text("Módulos", **TEXT_STYLES["breadcrumb_secondary_style"]),
                ft.Icon(
                    width=30,
                    height=30,
                    icon=ft.Icons.CHEVRON_RIGHT,
                    color=LIGHT_COLORS["secondary"],
                ),
                ft.Text(
                    "Módulo A: Ley de Enfriamiento de Newton",
                    **TEXT_STYLES["breadcrumb_primary_style"],
                ),
            ],
        )

        long_description = (
            "Este módulo de SnepThaw permite calcular las temperaturas de un líquido conductor "
            "utilizando la Ley de Enfriamiento de Newton. Este módulo es ideal para líquidos "
            "cuya temperatura puede ser considerada uniforme en todos sus puntos, como por "
            "ejemplo: el agua, café o similares."
        )

        title_and_desc = ft.Column(
            expand=2,
            controls=[
                ft.Text(
                    "Módulo A: Líquidos Simples", **TEXT_STYLES["page_title_style"]
                ),
                ft.Text(long_description, **TEXT_STYLES["page_description_style"]),
            ],
        )

        nmethod_and_other = ft.Column(
            expand=1,
            spacing=0,
            controls=[
                ft.Text("Método Numérico:", **TEXT_STYLES["suptitle_1_style"]),
                ft.Text("Método de Euler", **TEXT_STYLES["title_1_style"]),
            ],
        )

        main_content = ft.Row(
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[
                title_and_desc,
                ft.Container(width=30),
                nmethod_and_other,
            ],
        )

        self.content = ft.Column(
            expand=True,
            controls=[
                breadcrumbs,
                main_content,
            ],
        )


section_block_invisible_style: dict = {
    "expand": True,
    "padding": 30,
    "bgcolor": ft.Colors.WHITE,
    "border_radius": ft.BorderRadius(
        top_left=20,  # esquina superior izquierda sin redondear
        top_right=20,  # esquina superior derecha sin redondear
        bottom_left=20,  # esquina inferior izquierda redondeada
        bottom_right=20,  # esquina inferior derecha redondeada
    ),
}


section_block_style: dict = {
    "expand": True,
    "padding": 30,
    "bgcolor": ft.Colors.WHITE,
    "border_radius": ft.BorderRadius(
        top_left=20,  # esquina superior izquierda sin redondear
        top_right=20,  # esquina superior derecha sin redondear
        bottom_left=20,  # esquina inferior izquierda redondeada
        bottom_right=20,  # esquina inferior derecha redondeada
    ),
}


class GraphAndValuesBlock(ft.Container):
    def __init__(self):
        super().__init__(**section_block_style)


class SectionTitle(ft.Container):
    def __init__(self, section_label: str):
        super().__init__()

        self.section_label = section_label.upper()

        self.label = ft.Text(
            self.section_label,
            **TEXT_STYLES["section_title_style"],
        )

        self.content = ft.Row(
            expand=True,
            controls=[
                ft.Container(width=20),
                self.label,
                ft.Divider(**TEXT_STYLES["section_divider_style"]),
                ft.Container(width=20),
            ],
        )


def view(page: ft.Page):

    # COLUMNA CENTRAL __________________________________________________________
    # Todos los componentes de la página se colocan dentro de una columna
    # envuelta en un container que restringe su tamaño al 80% horizontal.

    central_column = ft.Container(
        content=ft.Column(
            controls=[
                TitleBlock(),
                SectionTitle("Mediciones"),
                SectionTitle("Gráficas y Valores Calculados"),
                GraphAndValuesBlock(),
                SectionTitle("Debug"),
                SectionTitle("Más información"),
                ft.ElevatedButton(
                    "Volver al inicio",
                    on_click=lambda _: asyncio.create_task(page.push_route("/")),
                ),
            ],
            spacing=15,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        # bgcolor=ft.Colors.RED,  ## DEBUG
        width=page.width * 0.9,  # 65% del ancho de la página
    )

    # CONTENIDO DE LA PÁGINA ___________________________________________________
    # La [columna central] se añade al View que se retona y se carga en main.py.
    # Todos los componentes están definidos más arriba en el código.
    # El ft.Row y los ft.Container que se agregan alrededor de la columna
    # central son para centrarla colocando espacios vacíos.

    content = ft.View(
        route="/ncl",
        controls=[
            ft.Row(
                controls=[
                    ft.Container(expand=True),
                    central_column,
                    ft.Container(expand=True),
                ],
                expand=True,
            )
        ],
        padding=0,
        bgcolor=LIGHT_COLORS["background"],
        scroll=ft.ScrollMode.AUTO,
    )

    return content
