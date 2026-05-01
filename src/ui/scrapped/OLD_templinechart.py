# COMPONENTE: Gráfico de línea para temperatura
# Este componente se usa para mostrar un gráfico de línea simple que
# representa la temperatura proyectada en un tiempo concreto.
# Es una versión modificada del LineChart del ejemplo del video.

from collections import namedtuple
from math import trunc
import flet as ft
import flet_charts as ftc
from src.ui.constants.theme_colors import DARK_COLORS
from src.calculations.data_types import TPoint
from src.calculations.time_manager import TimeManager


## Estructuras de datos
LineStyle = namedtuple(
    "LineStyle", ["line_color", "stroke_width", "selected_below_line_color"]
)

LabelsStyle = namedtuple(
    "LabelsStyle", ["x_label_color", "cant_labels_x", "y_label_color", "cant_labels_y"]
)


## Constantes
DEFAULT_LABELS_STYLE = LabelsStyle(DARK_COLORS["text"], 8, DARK_COLORS["text"], 8)


## Estilos
temp_chart_style: dict = {
    "expand": True,
    "tooltip": ftc.BarChartTooltip(
        bgcolor=ft.Colors.with_opacity(0.8, DARK_COLORS["text"])
    ),
    # "left_axis": ftc.ChartAxis(label_size=50, title_size=40),  # label_spacing=1
    # "bottom_axis": ftc.ChartAxis(label_size=50, title_size=40),
    "horizontal_grid_lines": ftc.ChartGridLines(
        interval=2, color=ft.Colors.with_opacity(0.2, DARK_COLORS["text"]), width=1
    ),
    "bgcolor": ft.Colors.TRANSPARENT,
}


## Clase
class TempLineChart(ftc.LineChart):
    def __init__(
        self,
        line_styles: list,
        labels_style: LabelsStyle = DEFAULT_LABELS_STYLE,
    ):
        print("<TempLineChart> Clase Instanciada...")
        super().__init__(
            **temp_chart_style,
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
            min_y=0,
            max_y=4,
            min_x=0,
            max_x=14,
        )

        self.line_styles = line_styles
        self.labels_style = labels_style
        # Lista de Listas de LineChartDataPoint
        self.points: list = [[] for _ in range(len(line_styles))]
        # Límites de los ejes
        self.min_x = None
        self.max_x = None
        self.min_y = None
        self.max_y = None

        # Cargar estilos de las líneas
        for i in range(0, len(line_styles)):
            self.data_series.append(
                ftc.LineChartData(
                    color=line_styles[i].line_color,
                    stroke_width=line_styles[i].stroke_width,
                    curved=True,
                    rounded_stroke_cap=True,
                    # Estilo de gradientes
                    below_line_gradient=ft.LinearGradient(
                        begin=ft.Alignment.TOP_CENTER,
                        end=ft.Alignment.BOTTOM_CENTER,
                        colors=[
                            ft.Colors.with_opacity(0.25, line_styles[i].line_color),
                            "transparent",
                        ],
                    ),
                    points=[],
                )
            )

    def update_labels(self, time_manager: TimeManager):
        x_labels = self.get_labels_for_time(
            self.labels_style.cant_labels_x,
            time_manager,
        )
        y_labels = self.get_labels_for_temp(self.labels_style.cant_labels_y)

        self.bottom_axis = ftc.ChartAxis(
            labels=x_labels.copy(),
            label_size=40,
        )

        self.left_axis = ftc.ChartAxis(
            labels=y_labels.copy(),
            label_size=60,
        )

    def load_points_from_tpoint_list(
        self, point_list: list[TPoint], serie_index: int, time_manager: TimeManager
    ):
        """Método que almacena una lista `point_list` de `TPoint` en la lista
        de puntos del gráfico de línea con id `serie_index` y luego lo actualiza para que se
        muestre en pantalla."""

        if len(point_list) > 50:
            print(f"WARNING: Too many coordinates ({len(point_list)})!!!")

        self.points[serie_index] = []  # Vaciar puntos.
        for i in range(0, len(point_list)):
            self.points[serie_index].append(
                ftc.LineChartDataPoint(
                    point_list[i].rtime,
                    point_list[i].temperature,
                    selected_below_line=ftc.ChartPointLine(
                        width=0.5,
                        color=self.line_styles[serie_index].selected_below_line_color,
                        dash_pattern=[2, 4],
                    ),
                    selected_point=ftc.ChartCirclePoint(stroke_width=1),
                ),
            )

        self.data_series[serie_index].points = self.points[serie_index].copy()
        self.update_labels(time_manager)
        self.update()

        print(
            f"\t<> func: load_points_from_tpoint_list(..., serie_index={serie_index}, ...)"
        )  # DEBUG
        self.print_tpoint_list(point_list)  # DEBUG
        self.print_loaded_points()  # DEBUG

    ## AUXILIARES
    def get_all_x_values(self):
        all_x = []
        for point_list in self.points:
            for lcdpoint in point_list:
                all_x.append(lcdpoint.x)
        return all_x

    def get_all_y_values(self):
        all_y = []
        for point_list in self.points:
            for lcdpoint in point_list:
                all_y.append(lcdpoint.y)
        return all_y

    def get_labels_for_temp(self, cant_labels: int):
        y_values = self.get_all_y_values()

        self.min_y = min(y_values)
        self.max_y = max(y_values)
        interval = (self.max_y - self.min_y) / cant_labels

        y_labels = []

        for i in range(0, cant_labels + 1):
            value = self.min_y + i * interval
            label_text: str = f"{round(value, 2)}°C"

            y_labels.append(
                ftc.ChartAxisLabel(
                    value=value,
                    label=ft.Text(
                        label_text  # , color=self.labels_style.y_label_color, size=12
                    ),
                )
            )

        print(f"\t<> func: get_labels_for_temp( cant_labels={cant_labels} )")  # DEBUG
        self.print_y_labels(y_labels)  # DEBUG
        return y_labels

    def get_labels_for_time(self, prefered_cant_labels: int, time_manager: TimeManager):
        x_values = self.get_all_x_values()

        series_interval = time_manager.interval

        self.min_x = min(x_values)
        self.max_x = max(x_values)

        raw_interval = (self.max_x - self.min_x) / prefered_cant_labels
        interval = round(raw_interval / series_interval, 0) * series_interval

        cant_labels = trunc((self.max_x - self.min_x) / interval)

        x_labels = []

        for i in range(0, cant_labels + 1):
            value = self.min_x + i * interval
            label_text: str = time_manager.format_relative_time(value)

            x_labels.append(
                ftc.ChartAxisLabel(
                    value=value,
                    label=ft.Text(
                        label_text  # , color=self.labels_style.x_label_color, size=12
                    ),
                )
            )

        print(
            f"\t<> func: get_labels_for_time( prefered_cant_labels={prefered_cant_labels} ...)"
        )  # DEBUG
        self.print_x_labels(x_labels)  # DEBUG
        return x_labels

    ## DEBUG
    def print_tpoint_list(self, tpoint_list: list[TPoint]):
        # Primeros 5
        for i in range(0, 5):
            tp = tpoint_list[i]
            print(f"\t\tTPoint({tp.rtime}\t, {tp.temperature})")
        print("\t\t...\t...")
        # Últimos 5
        for i in range(-4, 1):
            tp = tpoint_list[len(tpoint_list) - 1 + i]
            print(f"\t\tTPoint({tp.rtime}\t, {tp.temperature})")

    def print_loaded_points(self):
        for serie_index in range(0, len(self.points)):
            print(f"\t\tself.points[serie_index], \t serie_index = {serie_index}")

            if not self.points[serie_index]:
                print("\t\t\t---- EMPTY ----")
                break

            if len(self.points[serie_index]) < 5:
                for array_index in range(0, len(self.points[serie_index])):
                    print(
                        f"\t\t\tarray_index={len(self.points[serie_index]) + array_index - 1}",
                        f"\tL.C.D.Point({self.points[serie_index][array_index].x}\t, {self.points[serie_index][array_index].y})",
                    )
                break

            # Mostrar primeros 4...
            for array_index in range(0, 4):
                print(
                    f"\t\t\tarray_index={array_index}",
                    f"\tL.C.D.Point({self.points[serie_index][array_index].x}\t, {self.points[serie_index][array_index].y})",
                )

            print("\t\t\t ...")

            # Mostrar últimos 4...
            for array_index in range(-3, 1):
                print(
                    f"\t\t\tarray_index={len(self.points[serie_index]) + array_index - 1}",
                    f"\tL.C.D.Point({self.points[serie_index][array_index].x}\t, {self.points[serie_index][array_index].y})",
                )

    def print_x_labels(self, x_labels: list[ftc.ChartAxisLabel]):
        for lb in x_labels:
            print(
                f"\t\t\tx_label: lb.value='{lb.value}', label.value='{lb.label.value}'"
            )

    def print_y_labels(self, y_labels: list[ftc.ChartAxisLabel]):
        for lb in y_labels:
            print(
                f"\t\t\ty_label: lb.value='{lb.value}', label.value='{lb.label.value}'"
            )
