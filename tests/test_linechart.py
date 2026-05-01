import flet as ft
import flet_charts as ftc
from src.ui.constants.theme_colors import LIGHT_COLORS
import random
from src.calculations.data_types import TPoint
from src.calculations.time_manager import TimeManager


def create_example_series(
    cant: int, interval_x: float, min_x: float, min_y: float, max_y: float
):
    series = []

    for i in range(0, cant):
        x = min_x + interval_x * i
        y = min_y + (max_y - min_y) * random.random()
        p = ftc.LineChartDataPoint(x, y)
        series.append(p)

    return series


def main(page: ft.Page):
    # Configuraciones básicas
    page.title = "Página Principal"
    page.bgcolor = ft.Colors.GREY_700
    page.window.width = 800
    page.window.height = 600

    serie_1 = create_example_series(45, 0.25, 1, 0, 20)
    serie_2 = create_example_series(45, 0.25, 1, 0, 20)

    page.lc = ftc.LineChart(
        data_series=[
            ftc.LineChartData(
                points=serie_1,
                stroke_width=4,  # Ancho de la línea
                color=ft.Colors.CYAN,  # Color de la línea
                curved=True,  # Suaviza la línea (curva)
                rounded_stroke_cap=True,
            ),
            ftc.LineChartData(
                points=serie_2,
                stroke_width=4,  # Ancho de la línea
                color=ft.Colors.RED,  # Color de la línea
                curved=True,  # Suaviza la línea (curva)
                rounded_stroke_cap=True,
            ),
        ],
        left_axis=ftc.ChartAxis(
            labels=[
                ftc.ChartAxisLabel(value=1, label=ft.Text("1m")),
                ftc.ChartAxisLabel(value=1.5, label=ft.Text("1.5m")),
                ftc.ChartAxisLabel(value=2, label=ft.Text("2m")),
                ftc.ChartAxisLabel(value=2.5, label=ft.Text("2.5m")),
                ftc.ChartAxisLabel(value=3, label=ft.Text("3m")),
                ftc.ChartAxisLabel(value=3.5, label=ft.Text("3.5m")),
                ftc.ChartAxisLabel(value=4, label=ft.Text("4m")),
                ftc.ChartAxisLabel(value=4.5, label=ft.Text("4.5m")),
            ],
            label_size=40,  # Espacio reservado para las etiquetas
        ),
        bottom_axis=ftc.ChartAxis(
            labels=[
                ftc.ChartAxisLabel(value=2, label=ft.Text("SEP")),
                ftc.ChartAxisLabel(value=7, label=ft.Text("OCT")),
                ftc.ChartAxisLabel(value=12, label=ft.Text("DEC")),
            ],
            label_size=40,
        ),
        # Límites de los ejes (¡Importante!)
        min_y=0,
        max_y=4,
        min_x=0,
        max_x=14,
        expand=True,
    )

    page.add(
        ft.Column(
            expand=True,
            controls=[
                ft.Text(
                    "Test - LineChart",
                    font_family="Archivo",
                    size=36,
                    color=LIGHT_COLORS["text"],
                ),
                page.lc,
            ],
        )
    )

    page.update()


ft.app(target=main)
