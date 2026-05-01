import flet as ft
from src.ui.components.templinechart import TempLineChart, LineStyle
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
        p = TPoint(x, y)
        series.append(p)

    return series


line_styles = [  # "line_color", "stroke_width", "selected_below_line_color"
    LineStyle(
        LIGHT_COLORS["primary"],
        2,
        ft.Colors.with_opacity(0.2, LIGHT_COLORS["primary"]),
    ),
    LineStyle(
        LIGHT_COLORS["cold"],
        2,
        ft.Colors.with_opacity(0.2, LIGHT_COLORS["cold"]),
    ),
]


def main(page: ft.Page):
    # Configuraciones básicas
    page.title = "Página Principal"
    page.bgcolor = ft.Colors.GREY_700
    page.window.width = 800
    page.window.height = 600
    page.tlc = TempLineChart(line_styles)

    page.add(
        ft.Column(
            expand=True,
            controls=[
                ft.Text(
                    "Test - TempLineChart",
                    font_family="Archivo",
                    size=36,
                    color=LIGHT_COLORS["text"],
                ),
                page.tlc,
            ],
        )
    )

    tm = TimeManager(2)
    serie_1 = create_example_series(45, 0.25, 1, 0, 20)
    serie_2 = create_example_series(45, 0.25, 1, 0, 20)

    page.tlc.load_points_from_tpoint_list(serie_1, 0, tm)
    page.tlc.load_points_from_tpoint_list(serie_2, 1, tm)

    page.tlc.left_axis

    page.update()


ft.app(target=main)
