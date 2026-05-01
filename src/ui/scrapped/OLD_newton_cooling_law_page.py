# PÁGINA: Ley de Enfriamiento de Newton (PLAN A)
# En esta página el usuario puede ingresar las mediciones de temperatura y
# revisar la información y gráficos generados a partir de estas.
# NOTA: Solo es válido para líquidos muy conductores como el agua.


import flet as ft
from src.ui.components.templinechart import TempLineChart, LineStyle
from src.ui.constants.theme_colors import DARK_COLORS
from src.calculations.newton_cooling_law import NewtonCoolingLaw
from src.calculations.data_types import TPoint


general_container_style: dict = {
    "expand": True,
    "bgcolor": ft.Colors.with_opacity(0.06, DARK_COLORS["text"]),
    "border_radius": 10,
    "padding": 30,
}

section_title_style: dict = {
    "font_family": "DM Sans 14pt",
    "size": 24,
    "weight": "w300",
    "color": DARK_COLORS["text"],
}


class TempGraph(ft.Container):
    def __init__(self):
        super().__init__(**general_container_style)

        self.chart = (
            TempLineChart(  # "line_color", "stroke_width", "selected_below_line_color"
                line_styles=[
                    LineStyle(
                        DARK_COLORS["primary"],
                        2,
                        ft.Colors.with_opacity(0.2, DARK_COLORS["primary"]),
                    ),
                    LineStyle(
                        ft.Colors.with_opacity(0.6, DARK_COLORS["primary"]),
                        2,
                        ft.Colors.with_opacity(0.1, DARK_COLORS["primary"]),
                    ),
                ]
            )
        )
        self.content = ft.Column(
            expand=True,
            controls=[
                ft.Text("Proyección de Temperatura", **section_title_style),
                self.chart,
            ],
        )


current_temp_text_style: dict = {
    "font_family": "Archivo",
    "size": 48,
    "weight": "w500",  # Color depende de la temperatura
}

temp_rate_text_style: dict = {
    "font_family": "Archivo",
    "size": 48,
    "weight": "w500",  # Color depende de la temperatura
}

time_left_for_cooling_style: dict = {
    "font_family": "DM Sans 14pt",
    "size": 18,
    "weight": "w300",
    "color": DARK_COLORS["text"],
}


class CurrentTemp(ft.Container):
    def __init__(self):
        super().__init__(**general_container_style)

        # Texto que muestra la temperatura actual
        self.current_temp_text = ft.Text(
            "N/D°C", **current_temp_text_style, color=DARK_COLORS["text"]
        )

        # Texto que muestra la velocidad de temperatura actual
        self.temp_rate_text = ft.Text(
            "N/D°C/s", **temp_rate_text_style, color=DARK_COLORS["text"]
        )

        # Texto que muestra el tiempo restante para alcanzar
        # temperatura ambiente
        self.time_left_for_cooling = ft.Text(
            "No hay datos. Introduce medidas para calcular.",
            **time_left_for_cooling_style,
        )

        self.content = ft.Column(
            expand=True,
            spacing=0,
            # Por alguna razón tuve que añadir
            # esto porque ignora el expand=True...
            width=float("inf"),
            controls=[
                ft.Text("Temperatura Estimada", **section_title_style),
                self.current_temp_text,
                ft.Text("Tasa de Enfriamiento", **section_title_style),
                self.temp_rate_text,
                self.time_left_for_cooling,
            ],
        )


temp_measures_style: dict = {
    "main": {
        "expand": True,
        "bgcolor": "#17181d",
        "border_radius": 10,
    },
    "subtitle": {
        "font_family": "DM Sans 14pt",
        "size": 16,
        "weight": "w400",
        "color": DARK_COLORS["text"],
    },
    "input": {
        "width": 140,
        "height": 40,
        "color": DARK_COLORS["text"],
        "border_color": DARK_COLORS["secondary"],
        "cursor_height": 16,
        "cursor_color": DARK_COLORS["primary"],
        "content_padding": 10,
        "text_align": "center",
    },
    "add": {
        "icon": ft.Icons.ADD,
        "bgcolor": DARK_COLORS["primary"],
        "icon_size": 16,
        "icon_color": DARK_COLORS["background"],
        "scale": ft.Scale(0.8),
    },
    "data_table": {
        "columns": [  # Titulos de las columnas
            ft.DataColumn(
                ft.Text(
                    "Hora",
                    font_family="DM Sans 14pt",
                    weight="w900",
                    color=DARK_COLORS["primary"],
                )
            ),
            ft.DataColumn(
                ft.Text(
                    "Temperatura",
                    font_family="DM Sans 14pt",
                    weight="w900",
                    color=DARK_COLORS["primary"],
                ),
                numeric=True,
            ),
        ],
        "width": 380,
        "heading_row_height": 35,
        "data_row_max_height": 40,
    },
    "data_table_container": {
        "expand": True,
        "width": 450,
        "padding": 10,
        "border_radius": ft.BorderRadius.only(top_left=10, top_right=10),
        "bgcolor": ft.Colors.with_opacity(0.15, DARK_COLORS["primary"]),
    },
}


class TempMeasures(ft.Container):
    def __init__(self, ncl: NewtonCoolingLaw, temp_graph: TempGraph):
        super().__init__(**general_container_style)

        # Para acceder a los otros componentes, se los tenemos que enviar
        self.ncl = ncl
        self.temp_graph = temp_graph

        self.measure_input = ft.TextField(**temp_measures_style.get("input"))
        self.add_measure = ft.IconButton(
            **temp_measures_style.get("add"), on_click=lambda e: self.add_new_measure(e)
        )

        self.amb_temp_input = ft.TextField(**temp_measures_style.get("input"))
        self.add_amb_temp = ft.IconButton(
            **temp_measures_style.get("add"),
            on_click=lambda e: self.add_new_amb_temp(e),
        )

        self.measures_table = ft.DataTable(**temp_measures_style.get("data_table"))

        self.content = ft.Column(
            expand=True,
            controls=[
                ft.Text("Mediciones", **section_title_style),
                ft.Divider(height=5, color="transparent"),
                ft.Row(
                    expand=True,
                    controls=[
                        ft.Column(
                            expand=2,
                            controls=[
                                # Sección de INPUT de Mediciones de Temperatura
                                ft.Text(
                                    "Añadir medición",
                                    **temp_measures_style.get("subtitle"),
                                ),
                                ft.Row(
                                    controls=[
                                        self.measure_input,
                                        self.add_measure,
                                    ],
                                ),
                                # Sección de INPUT de Temperatura Ambiente
                                ft.Text(
                                    "Añadir temperatura ambiente",
                                    **temp_measures_style.get("subtitle"),
                                ),
                                ft.Row(
                                    controls=[
                                        self.amb_temp_input,
                                        self.add_amb_temp,
                                    ],
                                ),
                            ],
                        ),
                        ft.Column(
                            expand=3,
                            controls=[
                                ft.Container(
                                    **temp_measures_style.get("data_table_container"),
                                    content=ft.Column(
                                        expand=True,
                                        scroll="hidden",
                                        controls=[self.measures_table],
                                    ),
                                )
                            ],
                        ),
                    ],
                ),
            ],
        )

    def add_new_measure(self, event):
        """Método que se llama cuando se presiona el botón añadir. Añade la
        nueva temperatura a los componentes relacionados."""
        if self.measure_input.value != "" and self.measure_input.value.isdigit():
            new_temp: float = float(self.measure_input.value)
            self.ncl.add_measure(new_temp)
            self.measure_input.value = ""
            self.try_update_graph()

    def add_new_amb_temp(self, event):
        if self.amb_temp_input.value != "" and self.amb_temp_input.value.isdigit():
            new_amb_temp: float = float(self.amb_temp_input.value)
            self.ncl.add_amb_temp(new_amb_temp)
            self.amb_temp_input.value = ""
            self.try_update_graph()

    def update_measures_table(self, new_time, new_hour):
        """Método auxiliar que añade una medición a la tabla de mediciones."""

        ...

    def try_update_graph(self):
        if self.ncl.isReady():
            self.ncl.print_values()

            # Este solo muestra el verdadero, función solución
            p1 = self.ncl.get_prediction_with_function(self.ncl.intervals_ahead // 10)
            p2 = self.ncl.get_prediction_with_euler(self.ncl.intervals_ahead // 10)
            self.temp_graph.chart.load_points_from_tpoint_list(
                p1, 0, self.ncl.time_manager
            )
            self.temp_graph.chart.load_points_from_tpoint_list(
                p2, 1, self.ncl.time_manager
            )


small_title_style: dict = {
    "font_family": "DM Sans 14pt",
    "size": 16,
    "weight": "w300",
    "color": DARK_COLORS["text"],
}

value_title_style: dict = {
    "font_family": "DM Sans 14pt",
    "size": 20,
    "weight": "w400",
    "color": DARK_COLORS["primary"],
}

description_style: dict = {
    "font_family": "DM Sans 14pt",
    "size": 12,
    "weight": "w300",
    "color": DARK_COLORS["text"],
}


class OtherInfoAndValues(ft.Container):
    def __init__(self):
        super().__init__(**general_container_style)

        desc = (
            "La Ley de Enfriamiento de Newton es una ecuación diferencial "
            "ordinaria de primer orden que describe el enfriamiento de un objeto cuya "
            "temperatura se distribuye de forma uniforme. Es ideal para líquidos "
            "conductores como el agua."
        )

        self.content = ft.Column(
            expand=True,
            spacing=0,
            # Por alguna razón tuve que añadir esto porque ignora el expand=True...
            # width = float('inf'),
            controls=[
                ft.Text("Información General", **section_title_style),
                ft.Divider(height=15, color="transparent"),
                ft.Text("Ley Física:", **small_title_style),
                ft.Text("Ley de Enfriamiento de Newton", **value_title_style),
                ft.Text("Método Numérico:", **small_title_style),
                ft.Text("Método de Euler (step = 0.1)", **value_title_style),
                ft.Divider(height=15, color="transparent"),
                ft.Text(desc, **description_style),
            ],
        )


page_title_style: dict = {
    "font_family": "Archivo",
    "size": 24,
    "weight": "w600",
    "color": DARK_COLORS["secondary"],
}


def main(page: ft.Page):
    page.title = "SnepThaw | Escenario A: Líquidos Simples"
    page.padding = 30
    page.bgcolor = DARK_COLORS["background"]

    ### IMPORTANTE: El número que recibe el NCL es la cantidad de
    ### segundos que predice en el futuro. 900 segundos = 15 minutos
    page.ncl = NewtonCoolingLaw(900)

    # Creación de las 4 secciones
    temp_graph: ft.Container = TempGraph()
    current_temp: ft.Container = CurrentTemp()
    temp_measures: ft.Container = TempMeasures(page.ncl, temp_graph)
    other_info_and_values: ft.Container = OtherInfoAndValues()

    ## Estructura:
    ##       col 1             col 2
    ## [  temp_graph   ]  [ current_temp ]
    ## [ temp_measures ]  [ current_rate ]

    page.add(
        ft.Column(
            expand=True,
            controls=[
                ft.Text("ESCENARIO A: LÍQUIDOS SIMPLES", **page_title_style),
                ft.Row(
                    expand=True,
                    controls=[
                        ft.Column(
                            expand=3,  # Ocupará 3/5 del espacio
                            controls=[
                                temp_graph,
                                temp_measures,
                            ],
                        ),
                        ft.Column(
                            expand=2,  # Ocupará 2/5 del espacio
                            controls=[
                                current_temp,
                                other_info_and_values,
                            ],
                        ),
                    ],
                ),
            ],
        )
    )

    ## BORRAR: Ejemplo
    example_points = [
        TPoint(1, 40),
        TPoint(2, 35),
        TPoint(3, 30),
        TPoint(4, 26),
        TPoint(5, 23.5),
        TPoint(6, 21),
        TPoint(7, 19),
        TPoint(8, 17.5),
        TPoint(9, 15),
        TPoint(10, 14),
    ]
    temp_graph.chart.load_points_from_tpoint_list(
        example_points, 0, page.ncl.time_manager
    )

    page.update()
