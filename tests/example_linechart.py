# PÁGINA: Ejemplo de uso de LineChart con la librería flet_charts
# Esta página es solo de ejemplo y deberá desecharse en el producto final.
# Es una versión modificada (y actualizada) del video tutorial:
# https://youtu.be/EHN0aSkzcpA?si=7126iNHi8fvmgz-Q


import time

import flet as ft
import flet_charts as ftc
import locale # Se usa para darle formato a números

locale.setlocale(locale.LC_ALL, "en_US.UTF-8")



base_chart_style: dict = { # Estilo del gráfico de linea base
    "expand": True,
    "tooltip": ftc.BarChartTooltip(bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.WHITE)),
    "left_axis": ftc.ChartAxis(label_size=50),
    "bottom_axis": ftc.ChartAxis(label_spacing=1, title_size=40),
    "horizontal_grid_lines": ftc.ChartGridLines(
        interval=10,
        color=ft.Colors.with_opacity(0.2, ft.Colors.ON_SURFACE),
        width=1
    ),
    "bgcolor": ft.Colors.TRANSPARENT,
}

class BaseChart(ftc.LineChart):
    def __init__(self, line_color: str):
        super().__init__(**base_chart_style)

        # Crear lista vacía para guardar coordenadas
        self.points:list = []

        # Fijar el mínimo y máximo del eje X
        self.min_x = None
        self.max_x = None

        # Esta es la línea principal que se muestra en el UI
        self.line = ftc.LineChartData(
            color= line_color, #rojo para OUT y verde para IN
            stroke_width=2,
            curved=True,
            rounded_stroke_cap=True,
            # Estilo de gradientes
            below_line_gradient=ft.LinearGradient(
                begin=ft.Alignment.TOP_CENTER,
                end=ft.Alignment.BOTTOM_CENTER,
                colors=[
                    ft.Colors.with_opacity(0.25, line_color),
                    "transparent",
                ],
            ),
            points = self.points
        )

        self.data_series = [self.line]

    def update_axis_limits(self):
        if self.points:
            x_values = [point.x for point in self.points]
            y_values = [point.y for point in self.points]
            
            self.min_x = min(x_values)
            self.max_x = max(x_values)
            
            # Configurar límites del eje X
            self.bottom_axis.interval = max(1, (self.max_x - self.min_x) // 10)
            
            # Configurar límites del eje Y
            max_y = max(y_values)
            self.left_axis.max = max_y + (max_y * 0.1)  # Añadir 10% de margen    


    # Crear método que pone la info del Tracker a los graficos
    def create_data_points(self, x, y):
        self.points.append(
            ftc.LineChartDataPoint(
                x, y,
                selected_below_line=ftc.ChartPointLine(
                    width=0.5,
                    color="white54",
                    dash_pattern=[2, 4]
                ),
                selected_point=ftc.ChartCirclePoint(stroke_width=1),
            ),
        )
        
        self.line.data_points = self.points.copy()
        self.update_axis_limits()
        self.update()

in_style: dict = {
    "expand": 1,
    "bgcolor": "#17181d",
    "border_radius": 10,
    "padding": 30,
}

class GraphIn(ft.Container):
    def __init__(self):
        super().__init__(**in_style)
        self.chart = BaseChart(line_color="teal600")
        self.content = self.chart

out_style: dict = {
    "expand": 1,
    "bgcolor": "#17181d",
    "border_radius": 10,
    "padding": 30,
}

class GraphOut(ft.Container):
    def __init__(self):
        super().__init__(**out_style)
        self.chart = BaseChart(line_color="red500")
        self.content = self.chart


tracker_style: dict = {
    "main": {
        "expand": True,
        "bgcolor": "#17181d",
        "border_radius": 10,
    },
    "balance": {
        "size": 48,
        "weight": "bold",
    },
    "input": { # Estilo para cuadros de texto
        "width": 220,
        "height": 40,
        "border_color": "white12",
        "cursor_height": 16,
        "cursor_color": "white12",
        "content_padding": 10,
        "text_align": "center",
    },
    "add": { # Estilo para botón añadir
        "icon": ft.Icons.ADD,
        "bgcolor": "#1f2128",
        "icon_size": 16,
        "icon_color": "teal600",
        "scale": ft.Scale(0.8),
    },
    "subtract": { # Estilo para botón sustraer
        "icon": ft.Icons.REMOVE,
        "bgcolor": "#1f2128",
        "icon_size": 16,
        "icon_color": "red600",
        "scale": ft.Scale(0.8),
    },
    "data_table": { # Estilo para tabla de datos
        "columns": [ # Titulos de las columnas
            ft.DataColumn(ft.Text("Timestamp", weight="w900")),
            ft.DataColumn(ft.Text("Amount", weight="w900"),
                          numeric=True),
        ],
        "width": 380,
        "heading_row_height": 35,
        "data_row_max_height": 40,
    },
    "data_table_container": { # Estilo para el contenedor de la tabla
        "expand": True,
        "width": 450,
        "padding": 10,
        "border_radius": ft.BorderRadius.only(top_left=10, top_right=10),
        "shadow": ft.BoxShadow(
            spread_radius=8,
            blur_radius=15,
            color=ft.Colors.with_opacity(0.15, "black"),
            offset=ft.Offset(4,4),
        ),
        "bgcolor": ft.Colors.with_opacity(0.75, "#1f2128"),
    },
}

class Tracker(ft.Container):
    def __init__(self, _in: object, _out: object):
        super().__init__(**tracker_style.get("main"))
        self._in = _in
        self._out = _out

        self.counter = 0
        self.balance = ft.Text(
            locale.currency(self.counter, grouping=True),
            **tracker_style.get("balance")
        )

        self.input = ft.TextField(**tracker_style.get("input"))
        self.add = ft.IconButton(
            **tracker_style.get("add"),
            data=True,
            on_click = lambda e: self.update_balance(e)
        )
        self.subtract = ft.IconButton(
            **tracker_style.get("subtract"),
            data=False,
            on_click = lambda e: self.update_balance(e),
        )

        self.table = ft.DataTable(**tracker_style.get("data_table"))

        self.content = ft.Column(
            horizontal_alignment = "center",
            controls = [
                ft.Divider(height = 15, color = "transparent"),
                ft.Text("Totla Balance", size = 11, weight = "w900"),
                ft.Row(alignment = "center", controls=[self.balance]),
                ft.Divider(height = 15, color = "transparent"),
                ft.Row(
                    alignment="center", 
                    controls=[
                        self.subtract, 
                        self.input, 
                        self.add,
                    ],
                ),
                ft.Divider(height=25, color="transparent"),
                ft.Container(
                    **tracker_style.get("data_table_container"),
                    content=ft.Column(
                        expand=True,
                        scroll="hidden",
                        controls=[self.table],
                    )
                )
            ],
        )

        ## FOR SHOW PURPOSES
        self.x = 0

    # Primero, un método que actualice la tabla de datos
    def update_data_table(self, amount: float, sign: bool):
        timestamp = int(time.time())
        data = ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(timestamp)),
                ft.DataCell(
                    ft.Text(
                        locale.currency(amount, grouping=True),
                        color="teal" if sign else "red",
                        # La condición del color pondra un color segun el booleano sign
                    )
                ),
            ]
        )

        self.table.rows.append(data)
        self.table.update()

        return timestamp

    def update_balance(self, event):
        # 1. Comprobar que el valor ingresado no esta vacío y son digitos
        if self.input.value != "" and self.input.value.isdigit():
            # 2. Obtener el valor y parsearlo a float
            delta: float = float(self.input.value)
            # 3. Ver que botón fue presionado
            if event.control.data:
                self.counter += delta
                self.update_data_table(delta, sign=True)
                # Para mostrar las cantidades en los graficos, hacemos lo siguiente
                # _in es la instancia de GraphIN
                # chart es el self.chart en la clase base
                # create_data_point() es un método de BaseChart que crea una coordenada
                self._in.chart.create_data_points(
                    x=self.x,
                    y=delta,
                )
                self.x += 1
            else:
                self.counter -= delta
                self.update_data_table(delta, sign=False)
                # cambio de _in a _out
                self._out.chart.create_data_points(
                    x=self.x,
                    y=delta
                )
                self.x += 1
            
            # 4. Actualizar UI
            self.balance.value = locale.currency(
                self.counter,
                grouping=True
            )
            self.balance.update()
            self.input.value="" #Limpiar espacios
            self.input.update()


def main(page: ft.Page):
    page.padding = 30
    page.bgcolor = "#1f2128"

    graph_in: ft.Container = GraphIn()
    graph_out: ft.Container = GraphOut()
    tracker: ft.Container = Tracker(_in=graph_in, _out=graph_out)

    page.add(
        ft.Row(
            expand = True,
            controls = [
                tracker,
                ft.Column(
                    expand = True,
                    controls = [
                        graph_in,
                        graph_out
                    ],
                ),
            ],
        )
    )

    page.update()

if __name__ == "__main__":
    ft.app(target=main)