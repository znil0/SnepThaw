# PÁGINA: Ley de Enfriamiento de Newton (PLAN A) -Versión 2-
# En esta página el usuario puede ingresar las mediciones de temperatura y
# revisar la información y gráficos generados a partir de estas.
# NOTA: Solo es válido para líquidos muy conductores como el agua.

import flet as ft
import flet_charts as ftc
import asyncio

from src.ui.constants.theme_colors import LIGHT_COLORS, BASE_COLORS
from src.ui.constants.text_styles import TEXT_STYLES


# ESTILOS DE COMPONENTES _______________________________________________________
# Contiene las configuraciones de fuentes, layout, colores y otros relacionados
# con los bloques y componentes.

title_block_style: dict = {
    "expand": True,
    "padding": 30,
    "bgcolor": LIGHT_COLORS["background"],
    "border_radius": ft.BorderRadius(
        top_left=0,
        top_right=0,
        bottom_left=20,
        bottom_right=20,
    ),
}


section_block_invisible_style: dict = {
    "expand": True,
    "padding": 0,
    "bgcolor": ft.Colors.TRANSPARENT,
}


section_block_style: dict = {
    "expand": True,
    "padding": ft.Padding(30, 15, 30, 15),
    "bgcolor": LIGHT_COLORS["background"],
    "border_radius": ft.BorderRadius(
        top_left=20,  # esquina superior izquierda sin redondear
        top_right=20,  # esquina superior derecha sin redondear
        bottom_left=20,  # esquina inferior izquierda redondeada
        bottom_right=20,  # esquina inferior derecha redondeada
    ),
}


gav_chart_style: dict = {
    "expand": True,
    "tooltip": ftc.BarChartTooltip(
        bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.WHITE)
    ),
    "left_axis": ftc.ChartAxis(label_size=50),
    "bottom_axis": ftc.ChartAxis(label_spacing=1, title_size=40),
    "horizontal_grid_lines": ftc.ChartGridLines(
        interval=10, color=ft.Colors.with_opacity(0.2, ft.Colors.ON_SURFACE), width=1
    ),
    "bgcolor": ft.Colors.TRANSPARENT,
}


checkbox_style: dict = {
    "check_color": LIGHT_COLORS["background"],
    "active_color": LIGHT_COLORS["primary"],
    "border_side": ft.BorderSide(2, LIGHT_COLORS["primary"]),
}


footer_block_style: dict = {
    "expand": True,
    "padding": 30,
    "bgcolor": LIGHT_COLORS["background"],
    "border_radius": ft.BorderRadius(
        top_left=20,
        top_right=20,
        bottom_left=0,
        bottom_right=0,
    ),
}


# BLOQUE DE TÍTULO _____________________________________________________________
# Contiene el título y la descripción que se muestra en la parte superior
# de la página.


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
                    color=LIGHT_COLORS["primary"],
                ),
                ft.Text("Módulos", **TEXT_STYLES["breadcrumb_secondary_style"]),
                ft.Icon(
                    width=30,
                    height=30,
                    icon=ft.Icons.CHEVRON_RIGHT,
                    color=LIGHT_COLORS["primary"],
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


# BLOQUE DE MEDICIONES (Y SUS SUB-BLOQUES) _____________________________________
# Contiene toda la sección de mediciones, donde el usuario puede ingresar
# valores medidos y revisar aquellos que ya han sido introducidos.


class MeasuresBlock_Measures(ft.Container):
    def __init__(self):
        super().__init__(**section_block_style)
        self.expand = 2

        time_measure_field = ft.TextField(
            label="Tiempo Relativo (s)",
            label_style=ft.TextStyle(**TEXT_STYLES["measure_text_field_label_style"]),
            width=float("inf"),
            color=LIGHT_COLORS["text"],
            border_color=LIGHT_COLORS["primary"],
            text_style=ft.TextStyle(**TEXT_STYLES["measure_text_field_style"]),
        )

        temperature_measure_field = ft.TextField(
            label="Temperatura (°C)",
            label_style=ft.TextStyle(**TEXT_STYLES["measure_text_field_label_style"]),
            width=float("inf"),
            color=LIGHT_COLORS["text"],
            border_color=LIGHT_COLORS["primary"],
            text_style=ft.TextStyle(**TEXT_STYLES["measure_text_field_style"]),
        )

        submit_button = ft.Button(
            "Guardar",
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=LIGHT_COLORS["primary"],
                text_style=ft.TextStyle(
                    **TEXT_STYLES["submit_button_text_style"],
                ),
            ),
        )

        self.content = ft.Column(
            controls=[
                ft.Text("Añadir medición", **TEXT_STYLES["title_3_style"]),
                ft.Container(height=10),
                time_measure_field,
                temperature_measure_field,
                submit_button,
            ],
            expand=True,
        )


class MeasuresBlock_TimeNow(ft.Container):
    def __init__(self):
        super().__init__(**section_block_invisible_style)
        self.expand = 2

        self.time_text = ft.Text(
            "14:16:23",
            **TEXT_STYLES["big_value_2_style"],
        )

        self.rtime_text = ft.Text(
            "12 sec",
            **TEXT_STYLES["big_value_2_style"],
        )

        self.content = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("Hora actual", **TEXT_STYLES["title_3_style"]),
                            self.time_text,
                            ft.Text(
                                "según el sistema operativo",
                                **TEXT_STYLES["small_note_style"],
                            ),
                        ],
                        expand=True,
                        spacing=0,
                    ),
                    width=float("inf"),
                    **section_block_style,
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("Tiempo Relativo", **TEXT_STYLES["title_3_style"]),
                            self.rtime_text,
                            ft.Text(
                                "desde las 4:10:34",
                                **TEXT_STYLES["small_note_style"],
                            ),
                        ],
                        expand=True,
                        spacing=0,
                    ),
                    width=float("inf"),
                    **section_block_style,
                ),
            ],
            expand=True,
        )


class MeasuresBlock_Table(ft.Container):
    def __init__(self):
        super().__init__(**section_block_style)
        self.expand = 4

        self.table_values = [  # Placeholder
            {"tiempo_real": "1:30:45", "tiempo_relativo": 34, "temperatura": 23},
            {"tiempo_real": "1:36:23", "tiempo_relativo": 526, "temperatura": 12},
        ]

        self.datatable = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Hora Real", **TEXT_STYLES["table_label_style"])),
                ft.DataColumn(
                    ft.Text("Tiempo Relativo", **TEXT_STYLES["table_label_style"]),
                    numeric=True,
                ),
                ft.DataColumn(
                    ft.Text("Temperatura (°C)", **TEXT_STYLES["table_label_style"]),
                    numeric=True,
                ),
            ],
            rows=[],
        )

        self.set_values(self.table_values)

        self.content = ft.Column(
            controls=[
                ft.Text("Mediciones Almacenadas", **TEXT_STYLES["title_3_style"]),
                self.datatable,
            ],
            expand=True,
        )

    def set_values(self, value_list: list):
        self.table_values = value_list
        for value in value_list:
            self.datatable.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Text(
                                value["tiempo_real"],
                                **TEXT_STYLES["table_values_style"],
                            )
                        ),
                        ft.DataCell(
                            ft.Text(
                                str(value["tiempo_relativo"]),
                                **TEXT_STYLES["table_values_style"],
                            )
                        ),
                        ft.DataCell(
                            ft.Text(
                                str(value["temperatura"]),
                                **TEXT_STYLES["table_values_style"],
                            )
                        ),
                    ]
                )
            )

    def insert_value(self, atr1: str, atr2: str): ...


class MeasuresBlock(ft.Container):
    def __init__(self):
        super().__init__(**section_block_invisible_style)

        self.content = ft.Row(
            controls=[
                MeasuresBlock_Measures(),
                MeasuresBlock_TimeNow(),
                MeasuresBlock_Table(),
            ],
            height=260,
            ## Me rindo. No consigo que los hijos se expandan hacia arriba. La subsección
            ## MeasuresBlock_Measures siempre queda menos alta que la tabla...
            ## Te odio, Flet.
            expand=True,
        )


# BLOQUE DE GRÁFICOS Y VALORES _________________________________________________
# Contiene toda la sección de gráficos y las tablas de valores calculados.
# En esta sección se encuentra la gráfica principal que proporciona la
# proyección de temperatura respecto al tiempo al usuario.


class GAVChart(ftc.LineChart):
    def __init__(self, line_color_1: str, line_color_2):
        super().__init__(**gav_chart_style)

        self.points_1: list = []
        self.points_2: list = []

        self.min_x = None
        self.max_x = None

        self.line_1 = ftc.LineChartData(
            color=line_color_1,
            stroke_width=2,
            curved=True,
            rounded_stroke_cap=True,
            below_line_gradient=ft.LinearGradient(
                begin=ft.Alignment.TOP_CENTER,
                end=ft.Alignment.BOTTOM_CENTER,
                colors=[
                    ft.Colors.with_opacity(0.25, line_color_1),
                    "transparent",
                ],
            ),
            points=self.points_1,
        )

        self.line_2 = ftc.LineChartData(
            color=line_color_2,
            stroke_width=2,
            curved=True,
            rounded_stroke_cap=True,
            below_line_gradient=ft.LinearGradient(
                begin=ft.Alignment.TOP_CENTER,
                end=ft.Alignment.BOTTOM_CENTER,
                colors=[
                    ft.Colors.with_opacity(0.25, line_color_2),
                    "transparent",
                ],
            ),
            points=self.points_2,
        )

        self.data_series = [self.line_1, self.line_2]

    def update_axis_limits(self):
        if self.points_1:
            x_values = [point.x for point in self.points_1]
            y_values = [point.y for point in self.points_1]

            self.min_x = min(x_values)
            self.max_x = max(x_values)

            # Configurar límites del eje X
            self.bottom_axis.interval = max(1, (self.max_x - self.min_x) // 10)

            # Configurar límites del eje Y
            max_y = max(y_values)
            self.left_axis.max = max_y + (max_y * 0.1)  # Añadir 10% de margen

        if self.points_2:
            x_values = [point.x for point in self.points_2]
            y_values = [point.y for point in self.points_2]

            self.min_x = min(x_values)
            self.max_x = max(x_values)

            # Configurar límites del eje X
            self.bottom_axis.interval = max(1, (self.max_x - self.min_x) // 10)

            # Configurar límites del eje Y
            max_y = max(y_values)
            self.left_axis.max = max_y + (max_y * 0.1)  # Añadir 10% de margen

    def create_data_points(self, x, y, line: int):
        if line == 1:
            self.points_1.append(
                ftc.LineChartDataPoint(
                    x,
                    y,
                    selected_below_line=ftc.ChartPointLine(
                        width=0.5, color="white54", dash_pattern=[2, 4]
                    ),
                    selected_point=ftc.ChartCirclePoint(stroke_width=1),
                ),
            )

            self.line_1.data_points = self.points_1.copy()
        if line == 2:
            self.points_2.append(
                ftc.LineChartDataPoint(
                    x,
                    y,
                    selected_below_line=ftc.ChartPointLine(
                        width=0.5, color="white54", dash_pattern=[2, 4]
                    ),
                    selected_point=ftc.ChartCirclePoint(stroke_width=1),
                ),
            )

            self.line_2.data_points = self.points_2.copy()
        self.update_axis_limits()
        self.update()


class GraphAndValuesBlock_Graph(ft.Container):
    def __init__(self):
        super().__init__(**section_block_style)
        self.expand = 3

        self.graph = GAVChart(BASE_COLORS["color_3"], BASE_COLORS["color_4"])

        self.content = self.graph


class GraphAndValuesBlock_Predicted(ft.Container):
    def __init__(self):
        super().__init__(**section_block_invisible_style)
        self.expand = 1

        # Temperatura Estimada
        self.predicted_temperature = ft.Text(
            "35°C",
            **TEXT_STYLES["big_value_1_style"],
        )

        predicted_temperature_block = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Temperatura Estimada", **TEXT_STYLES["title_3_style"]),
                    self.predicted_temperature,
                ],
                expand=True,
                spacing=0,
            ),
            width=float("inf"),
            **section_block_style,
        )

        # Tasa de Enfriamiento
        self.cooling_rate = ft.Text(
            "-1.2°C/s",
            **TEXT_STYLES["big_value_1_style"],
        )

        cooling_rate_block = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Tasa de Enfriamiento", **TEXT_STYLES["title_3_style"]),
                    self.cooling_rate,
                ],
                expand=True,
                spacing=0,
            ),
            width=float("inf"),
            **section_block_style,
        )

        # Tiempo hasta enfriamiento
        self.time_left = ft.Text(
            "1h 23m 45s",
            **TEXT_STYLES["big_value_2_style"],
        )

        time_left_block = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Enfriamento en:", **TEXT_STYLES["title_3_style"]),
                    self.time_left,
                ],
                expand=True,
                spacing=0,
            ),
            width=float("inf"),
            **section_block_style,
        )

        self.content = ft.Column(
            controls=[
                predicted_temperature_block,
                cooling_rate_block,
                time_left_block,
            ],
            expand=True,
        )


class GraphAndValuesBlock(ft.Container):
    def __init__(self):
        super().__init__(**section_block_invisible_style)

        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        GraphAndValuesBlock_Graph(),
                        GraphAndValuesBlock_Predicted(),
                    ],
                    height=450,
                    expand=True,
                )
            ],
            expand=True,
        )


# BLOQUE DE OPCIONES AVANZADAS _________________________________________________
# Contiene un panel de opciones que permiten habilitar ciertas herramientas
# con propósitos de desarrollo y testeo.


class DebugBlock(ft.Container):
    def __init__(self):
        super().__init__(**section_block_style)

        self.chk_show_relative_time_field = ft.Checkbox(
            ft.Text(
                "Permitir ingresar tiempos relativos",
                **TEXT_STYLES["checkbox_label_style"],
            ),
            **checkbox_style,
        )

        self.content = ft.Column(
            controls=[
                ft.Text(
                    "Opciones Avanzadas (De Prueba)", **TEXT_STYLES["title_3_style"]
                ),
                self.chk_show_relative_time_field,
            ],
            expand=True,
        )


# BLOQUE DE MÁS INFORMACIÓN ____________________________________________________
# Contiene el footer de la página, mismo que muestra información adicional
# la misma.


class MoreInfoBlock(ft.Container):
    def __init__(self, page):
        super().__init__(**footer_block_style)

        footer_description = "Aquí va información, UwU"

        self.content = ft.Column(
            controls=[
                ft.Text(footer_description, **TEXT_STYLES["page_description_style"]),
                ft.ElevatedButton(
                    "Volver al inicio",
                    on_click=lambda _: asyncio.create_task(page.push_route("/")),
                ),
            ],
            width=float("inf"),
            expand=True,
        )


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
                ft.Icon(**TEXT_STYLES["section_divider_icon_style"]),
                # ft.Container(width=20),
                self.label,
                ft.Divider(**TEXT_STYLES["section_divider_style"]),
                # ft.Container(width=20),
            ],
            margin=ft.Margin(0, 20, 0, 0),
        )


# VIEW PRINCIPAL _______________________________________________________________
# Este es el lugar donde toda la página se ensambla. Debido a limitaciones del
# propio flet, la verdadera Page se encuentra en el módulo `main.py`. Este view
# agrupa todos los componentes y sus layouts para que `main.py` las muestre
# correctamente y las maneje según los botones que presione el usuario.


def view(page: ft.Page):

    # COLUMNA CENTRAL __________________________________________________________
    # Todos los componentes de la página se colocan dentro de una columna
    # envuelta en un container que restringe su tamaño al 80% horizontal.

    central_column = ft.Container(
        content=ft.Column(
            controls=[
                TitleBlock(),
                SectionTitle("Mediciones de Temperatura"),
                MeasuresBlock(),
                SectionTitle("Gráficas y Valores Calculados"),
                GraphAndValuesBlock(),
                SectionTitle("Debug"),
                DebugBlock(),
                SectionTitle("Más información"),
                MoreInfoBlock(page),
            ],
            spacing=15,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        # bgcolor=ft.Colors.RED,  ## DEBUG
        width=page.width * 0.8,  # 80% del ancho de la página
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
        bgcolor=LIGHT_COLORS["background_2"],
        scroll=ft.ScrollMode.AUTO,
    )

    return content
