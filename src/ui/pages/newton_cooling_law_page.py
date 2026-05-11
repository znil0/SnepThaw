# PÁGINA: Ley de Enfriamiento de Newton (PLAN A) -Versión 2-
# En esta página el usuario puede ingresar las mediciones de temperatura y
# revisar la información y gráficos generados a partir de estas.
# NOTA: Solo es válido para líquidos muy conductores como el agua.

import flet as ft
import flet_charts as ftc
import asyncio
import random
import math

from src.ui.constants.theme_colors import LIGHT_COLORS, BASE_COLORS
from src.ui.constants.text_styles import TEXT_STYLES

from src.calculations.time_manager import TimeManager
from src.calculations.data_types import TempMeasure, TPoint
from src.calculations.newton_cooling_law import NewtonCoolingLaw


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
    "shadow": ft.BoxShadow(
        spread_radius=1,
        blur_radius=3,
        color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
        offset=ft.Offset(2, 4),  # Desplazamiento en x, y
    ),
}


section_block_invisible_style: dict = {
    "expand": True,
    "padding": 0,
    "bgcolor": ft.Colors.TRANSPARENT,
    "animate": ft.Animation(500, ft.AnimationCurve.EASE_IN_OUT),
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
    "shadow": ft.BoxShadow(
        spread_radius=1,
        blur_radius=3,
        color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
        offset=ft.Offset(2, 4),  # Desplazamiento en x, y
    ),
    "animate": ft.Animation(500, ft.AnimationCurve.EASE_IN_OUT),
}


gav_chart_style: dict = {
    "expand": True,
    "tooltip": ftc.BarChartTooltip(
        bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.WHITE)
    ),
    "left_axis": ftc.ChartAxis(
        ft.Text(
            "Temperatura del líquido (°C)",
            **TEXT_STYLES["gav_chart_title_style"],
        ),
        label_size=30,
        title_size=30,
    ),
    "bottom_axis": ftc.ChartAxis(
        ft.Text(
            "Tiempo relativo (s)",
            **TEXT_STYLES["gav_chart_title_style"],
        ),
        # label_spacing=1,
        label_size=24,
        title_size=30,
    ),
    "horizontal_grid_lines": ftc.ChartGridLines(
        interval=10, color=ft.Colors.with_opacity(0.2, ft.Colors.ON_SURFACE), width=1
    ),
    "bgcolor": ft.Colors.TRANSPARENT,
    # "margin": ft.Margin(30, 30, 30, 30),
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
    "margin": ft.Margin(0, 40, 0, 0),
    "shadow": ft.BoxShadow(
        spread_radius=1,
        blur_radius=3,
        color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
        offset=ft.Offset(2, 4),  # Desplazamiento en x, y
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


# TÍTULO DE SECCIÓN ____________________________________________________________
# Contiene el título de la sección y permite colapsar (ocultar) el contenido de
# la misma mediante el chevron que tiene al inicio.


class SectionTitle(ft.Container):
    def __init__(self, section_label: str, block: ft.Container):
        super().__init__()

        self.section_label = section_label.upper()

        self.label = ft.Text(
            self.section_label,
            **TEXT_STYLES["section_title_style"],
        )

        self.chevron = ft.IconButton(
            icon=ft.Icon(**TEXT_STYLES["section_divider_icon_style"]),
            animate_rotation=ft.Animation(500, ft.AnimationCurve.EASE_IN_OUT),
            rotate=3.14159,
            on_click=self.toggle_visibility,
        )
        self.block = block
        self.contracted = False

        self.content = ft.Row(
            expand=True,
            controls=[
                self.chevron,
                self.label,
                ft.Divider(**TEXT_STYLES["section_divider_style"]),
            ],
            # margin=ft.Margin(0, 20, 0, 0),
        )

    async def toggle_visibility(self, e):
        c = self.block

        self.contracted = not self.contracted

        self.page.update()

        # Girar Chevron: 0° -> 90°
        self.chevron.rotate = 3.14159 / 2 if self.contracted else 3.14159

        # Cambiar altura: 100px -> 0px
        c.height = 0 if self.contracted else self.block.content_height

        self.page.update()

        # Ocultar el contenido cuando está contraído
        if self.contracted:
            await asyncio.sleep(0.5)  # 500 ms
        c.content.visible = not self.contracted

        self.page.update()


# BLOQUE DE CONFIGURACIÓN DE PREDICCIONES ______________________________________
# Contiene toda la sección de mediciones, donde el usuario puede ingresar
# valores medidos y revisar aquellos que ya han sido introducidos.


class NCLConfigBlock(ft.Container):
    def __init__(self):
        super().__init__(**section_block_invisible_style)

        self.content_height = 350
        self.height = self.content_height

        ## VENTANA EMERGENTE: execute_ncl no se puede deshacer
        def yes_action():
            global seconds_ahead
            seconds_ahead = int(self.seconds_ahead_field.value)
            global ncl_update_intervals
            ncl_update_intervals = int(self.update_intervals_field.value)
            global ncl
            ncl = NewtonCoolingLaw(seconds_ahead)
            time_manager.reset_start_time()
            ncl.set_time_manager(time_manager)

            self.disable_execute_ncl_button_and_fields()
            self.permanent_ncl_dialog.open = False

            # DEBUG
            print(
                "<NCLConfigBlock> Instanciated NCL with: \n"
                + f"\t seconds_ahead -> {seconds_ahead}"
            )

            print(
                f"<NCLConfigBlock> Stored value 'ncl_update_intervals -> {ncl_update_intervals}'"
            )

        def no_action():
            self.permanent_ncl_dialog.open = False

        self.permanent_ncl_dialog = ft.AlertDialog(
            modal=True,  # Obligatorio responder
            bgcolor=LIGHT_COLORS["background"],
            title=ft.Text(
                "Acción permanente",
                **TEXT_STYLES["alert_dialog_title_style"],
            ),
            content=ft.Text(
                "Por limitaciones del método implementado, una vez iniciado el módulo NCL \n"
                + "sus parámetros no pueden ser modificados sin reiniciar el programa. Desea \n"
                + "continuar?",
                **TEXT_STYLES["alert_dialog_description_style"],
            ),
            actions=[
                ft.TextButton(
                    ft.Text(
                        "Sí, iniciar módulo",
                        **TEXT_STYLES["alert_dialog_textbutton_style"],
                    ),
                    on_click=yes_action,
                ),
                ft.TextButton(
                    ft.Text(
                        "No, cancelar",
                        **TEXT_STYLES["alert_dialog_textbutton_style"],
                    ),
                    on_click=no_action,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,  # Alinea los botones a la derecha
        )

        # SECCIÓN DE PARAMETROS

        self.seconds_ahead_field = ft.TextField(
            label="seconds_ahead",
            label_style=ft.TextStyle(**TEXT_STYLES["measure_text_field_label_style"]),
            width=float("inf"),
            color=LIGHT_COLORS["text"],
            border_color=LIGHT_COLORS["primary"],
            text_style=ft.TextStyle(**TEXT_STYLES["measure_text_field_style"]),
        )

        self.update_intervals_field = ft.TextField(
            label="update_intervals",
            label_style=ft.TextStyle(**TEXT_STYLES["measure_text_field_label_style"]),
            width=float("inf"),
            color=LIGHT_COLORS["text"],
            border_color=LIGHT_COLORS["primary"],
            text_style=ft.TextStyle(**TEXT_STYLES["measure_text_field_style"]),
        )

        self.execute_ncl_button = ft.Button(
            "Ejecutar módulo NCL",
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=LIGHT_COLORS["primary"],
                text_style=ft.TextStyle(
                    **TEXT_STYLES["submit_button_text_style"],
                ),
            ),
            on_click=self.on_click_execute_ncl,
        )

        parameters_block = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Parámetros de cálculo",
                        **TEXT_STYLES["title_3_style"],
                    ),
                    ft.Text(
                        "Parámetro que define la cantidad de segundos a predecir con cada iteración.",
                        **TEXT_STYLES["small_title_style"],
                    ),
                    self.seconds_ahead_field,
                    ft.Text(
                        "Parámetro que define la cantidad de ticks a saltar antes de actualizar la gráfica. (8 ticks = 1 segundo).",
                        **TEXT_STYLES["small_title_style"],
                    ),
                    self.update_intervals_field,
                    self.execute_ncl_button,
                ],
                expand=True,
            ),
            **section_block_style,
        )
        parameters_block.expand = 1

        # SECCIÓN DE VALORES CALCULADOS
        self.intervals_ahead_text = ft.Text(
            "No instanciado",
            **TEXT_STYLES["small_value_1_style"],
        )
        self.measure_1_text = ft.Text(
            "No instanciado",
            **TEXT_STYLES["small_value_1_style"],
        )
        self.measure_2_text = ft.Text(
            "No instanciado",
            **TEXT_STYLES["small_value_1_style"],
        )
        self.amb_temp_text = ft.Text(
            "No instanciado",
            **TEXT_STYLES["small_value_1_style"],
        )
        self.r_text = ft.Text(
            "No instanciado",
            **TEXT_STYLES["small_value_1_style"],
        )
        self.is_ready_text = ft.Text(
            "No instanciado",
            **TEXT_STYLES["small_value_1_style"],
        )

        calculated_block = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Constantes y valores calculados",
                        **TEXT_STYLES["title_3_style"],
                    ),
                    ft.Container(height=10),
                    ft.Text(
                        "intervals_ahead (Intervalos a Medir)",
                        **TEXT_STYLES["small_value_1_label_style"],
                    ),
                    self.intervals_ahead_text,
                    ft.Text(
                        "measure_1 (Primera Medición)",
                        **TEXT_STYLES["small_value_1_label_style"],
                    ),
                    self.measure_1_text,
                    ft.Text(
                        "measure_2 (Segunda Medición)",
                        **TEXT_STYLES["small_value_1_label_style"],
                    ),
                    self.measure_2_text,
                    ft.Text(
                        "amb_temp (Temperatura Ambiente)",
                        **TEXT_STYLES["small_value_1_label_style"],
                    ),
                    self.amb_temp_text,
                    ft.Text(
                        "r (Coeficiente de Enfriamiento)",
                        **TEXT_STYLES["small_value_1_label_style"],
                    ),
                    self.r_text,
                    ft.Text(
                        "isReady (Flag de Estado)",
                        **TEXT_STYLES["small_value_1_label_style"],
                    ),
                    self.is_ready_text,
                ],
                expand=True,
                spacing=0,
            ),
            **section_block_style,
        )
        calculated_block.expand = 2

        self.content = ft.Row(
            controls=[
                parameters_block,
                calculated_block,
            ],
            height=self.content_height,
            expand=True,
        )

    def on_click_execute_ncl(self):
        self.permanent_ncl_dialog.open = True

    def disable_execute_ncl_button_and_fields(self):
        # Desactivar botón
        self.execute_ncl_button.disable = True
        self.execute_ncl_button.content = "Instanciado"
        self.execute_ncl_button.style = self.disabled_button_style = ft.ButtonStyle(
            color=ft.Colors.with_opacity(0.5, LIGHT_COLORS["primary"]),
            bgcolor=LIGHT_COLORS["background"],
            side=ft.BorderSide(2, ft.Colors.with_opacity(0.5, LIGHT_COLORS["primary"])),
            shape=ft.RoundedRectangleBorder(radius=5),
            text_style=ft.TextStyle(
                **TEXT_STYLES["submit_button_text_style"],
            ),
        )

        # Desactivar labels
        self.seconds_ahead_field.disabled = True
        self.seconds_ahead_field.bgcolor = LIGHT_COLORS["background_2"]
        self.update_intervals_field.disabled = True
        self.update_intervals_field.bgcolor = LIGHT_COLORS["background_2"]

    def update_calculated_values(self):
        global ncl
        if ncl is not None:
            self.intervals_ahead_text.value = str(ncl.intervals_ahead)
            self.measure_1_text.value = str(ncl.measure_1)
            self.measure_2_text.value = str(ncl.measure_2)
            self.amb_temp_text.value = str(ncl.amb_temp)
            self.r_text.value = str(ncl.r)
            self.is_ready_text.value = str(ncl.is_ready())


# BLOQUE DE MEDICIONES (Y SUS SUB-BLOQUES) _____________________________________
# Contiene toda la sección de mediciones, donde el usuario puede ingresar
# valores medidos y revisar aquellos que ya han sido introducidos.


class MeasuresBlock_Measures(ft.Container):
    def __init__(self, ncl_not_defined_dialog: ft.AlertDialog):
        super().__init__(**section_block_style)

        self.ncl_not_defined_dialog = ncl_not_defined_dialog
        self.expand = 1

        self.time_measure_field = ft.TextField(
            label="Tiempo Relativo (s)",
            label_style=ft.TextStyle(**TEXT_STYLES["measure_text_field_label_style"]),
            width=float("inf"),
            color=LIGHT_COLORS["text"],
            border_color=LIGHT_COLORS["primary"],
            text_style=ft.TextStyle(**TEXT_STYLES["measure_text_field_style"]),
        )

        self.temperature_measure_field = ft.TextField(
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
            on_click=self.set_measure,
        )

        self.content = ft.Column(
            controls=[
                ft.Text("Añadir medición", **TEXT_STYLES["title_3_style"]),
                ft.Container(height=10),
                self.time_measure_field,
                self.temperature_measure_field,
                submit_button,
            ],
            expand=True,
        )

    def set_mb_table(self, mb_table: ft.Container):
        self.mb_table = mb_table

    def set_measure(self):

        # Obtener tiempo relativo
        if self.time_measure_field.visible:
            rtime = float(self.time_measure_field.value)
        else:
            rtime = time_manager.get_relative_time()
        rtime = time_manager.round_to_interval(rtime)

        # Obtener temperatura
        temp = float(self.temperature_measure_field.value)

        # Ensamblar TempMeasure y mostrarlo en tabla
        temp_measure = TempMeasure(time_manager.relative_time_to_timestamp(rtime), temp)
        print(  # Debug
            "<MeasuresBlock: Measures> CREATED MEASURE: ",
            f"\n\ttemp_measure.timestamp -> {temp_measure.timestamp}",
            f"\n\ttemp_measure.temperature -> {temp_measure.temperature}",
        )

        # ENVIAR MEDICIÓN A NCL
        global ncl
        if ncl is not None:
            ncl.add_measure(temp_measure)

            self.time_measure_field.value = ""
            self.temperature_measure_field.value = ""
            self.mb_table.insert_temp_measure(temp_measure)
        else:
            self.ncl_not_defined_dialog.open = True


class MeasuresBlock_TimeNow(ft.Container):
    def __init__(self):
        super().__init__(**section_block_invisible_style)
        self.expand = 1

        self.time_text = ft.Text(
            "HH:MM:SS",
            **TEXT_STYLES["big_value_2_style"],
        )

        self.rtime_text = ft.Text(
            "N/D sec",
            **TEXT_STYLES["big_value_2_style"],
        )

        self.rtime_since_text = ft.Text(
            "desde las HH:MM:SS",
            **TEXT_STYLES["small_note_style"],
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
                            self.rtime_since_text,
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
        self.expand = 2

        self.placeholder_deleted = False
        self.table_values = [  # Placeholder
            {
                "tiempo_real": "HH:MM:SS (24 hr format)",
                "tiempo_relativo": "N/D",
                "temperatura": "N/D",
            },
        ]

        self.datatable = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Hora Real", **TEXT_STYLES["table_label_style"])),
                ft.DataColumn(
                    ft.Text("Tiempo Relativo (s)", **TEXT_STYLES["table_label_style"]),
                    numeric=True,
                ),
                ft.DataColumn(
                    ft.Text("Temperatura (°C)", **TEXT_STYLES["table_label_style"]),
                    numeric=True,
                ),
            ],
            rows=[],
        )

        # Configuraciones iniciales: Placeholder y disabled
        self.set_values(self.table_values)
        self.placeholder_deleted = False

        self.content = ft.Column(
            controls=[
                ft.Text("Mediciones Almacenadas", **TEXT_STYLES["title_3_style"]),
                self.datatable,
            ],
            expand=True,
        )

    def set_placeholder(self):
        self.table_values = [
            {
                "tiempo_real": "HH:MM:SS (24 hr format)",
                "tiempo_relativo": "N/D",
                "temperatura": "N/D",
            },
        ]
        self.set_values(self.table_values)
        self.placeholder_deleted = False

    def set_mb_options(self, mb_options: ft.Container):
        self.mb_options = mb_options

    def set_values(self, value_list: list):
        self.placeholder_deleted = True
        self.datatable.rows = []
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

    def insert_value(self, real_time: float, r_time: float, temperature: float):

        if not self.placeholder_deleted:
            self.placeholder_deleted = True
            self.table_values = []
            self.datatable.rows = []
            self.mb_options.toggle_datatable_buttons()

        self.datatable.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(
                        ft.Text(
                            str(real_time),
                            **TEXT_STYLES["table_values_style"],
                        )
                    ),
                    ft.DataCell(
                        ft.Text(
                            str(r_time),
                            **TEXT_STYLES["table_values_style"],
                        )
                    ),
                    ft.DataCell(
                        ft.Text(
                            str(temperature),
                            **TEXT_STYLES["table_values_style"],
                        )
                    ),
                ]
            )
        )

    def insert_temp_measure(self, temp_measure: TempMeasure):
        relative_time = time_manager.get_relative_time(temp_measure.timestamp)
        real_time = time_manager.format_relative_time(relative_time, 5)
        temperature = temp_measure.temperature

        self.insert_value(real_time, relative_time, temperature)

    def delete_last_value(self):
        self.datatable.rows.pop()
        if len(self.datatable.rows) == 0:
            return True  # si quedo vacia
        return False


class MeasuresBlock_AmbientalConditions(ft.Container):
    def __init__(self):
        super().__init__(**section_block_style)
        self.expand = 1

        self.amb_temp_measure_field = ft.TextField(
            label="Temperatura Ambiente (°C)",
            label_style=ft.TextStyle(**TEXT_STYLES["measure_text_field_label_style"]),
            width=float("inf"),
            color=LIGHT_COLORS["text"],
            border_color=LIGHT_COLORS["primary"],
            text_style=ft.TextStyle(**TEXT_STYLES["measure_text_field_style"]),
        )

        self.amb_temp_text = ft.Text(
            "No definida",
            **TEXT_STYLES["big_value_3_style"],
        )

        self.submit_button = ft.Button(
            "Fijar Temperatura Ambiente",
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=LIGHT_COLORS["primary"],
                text_style=ft.TextStyle(
                    **TEXT_STYLES["submit_button_text_style"],
                ),
            ),
            on_click=self.set_amb_temp,
        )

        self.content = ft.Column(
            controls=[
                ft.Text("Temperatura Ambiente", **TEXT_STYLES["title_3_style"]),
                # ft.Container(height=10),
                self.amb_temp_text,
                self.amb_temp_measure_field,
                self.submit_button,
            ],
            expand=True,
        )

    def set_amb_temp(self):
        amb_temp = float(self.amb_temp_measure_field.value)
        self.amb_temp_measure_field.value = ""

        self.amb_temp_text.value = f"{amb_temp}°C"

        # ENVIAR TEMPERATURA AMBIENTE A NCL
        global ncl
        ncl.add_amb_temp(amb_temp)


class MeasuresBlock_Options(ft.Container):
    def __init__(self, reset_timer_dialog: ft.AlertDialog):
        super().__init__(**section_block_style)
        self.reset_timer_dialog = reset_timer_dialog
        self.expand = 1

        self.button_style = ft.ButtonStyle(
            color=LIGHT_COLORS["primary"],
            bgcolor=LIGHT_COLORS["background"],
            side=ft.BorderSide(2, LIGHT_COLORS["primary"]),
            shape=ft.RoundedRectangleBorder(radius=5),
            text_style=ft.TextStyle(
                **TEXT_STYLES["submit_button_text_style"],
            ),
        )

        self.disabled_button_style = ft.ButtonStyle(
            color=ft.Colors.with_opacity(0.5, LIGHT_COLORS["primary"]),
            bgcolor=LIGHT_COLORS["background"],
            side=ft.BorderSide(2, ft.Colors.with_opacity(0.5, LIGHT_COLORS["primary"])),
            shape=ft.RoundedRectangleBorder(radius=5),
            text_style=ft.TextStyle(
                **TEXT_STYLES["submit_button_text_style"],
            ),
        )

        self.delete_last_measure_button = ft.Button(
            "Eliminar última medición",
            disabled=True,
            style=self.disabled_button_style,
            on_click=self.delete_last_measure,
        )

        self.empty_table_button = ft.Button(
            "Vaciar tabla de mediciones",
            disabled=True,
            style=self.disabled_button_style,
            on_click=self.empty_datatable,
        )

        reset_timer_button = ft.Button(
            "Reiniciar Cronómetro",
            style=self.button_style,
            on_click=self.reset_time_manager,
        )

        self.content = ft.Column(
            controls=[
                ft.Text("Opciones", **TEXT_STYLES["title_3_style"]),
                ft.Container(height=10),
                self.delete_last_measure_button,
                self.empty_table_button,
                reset_timer_button,
            ],
            expand=True,
        )

    def toggle_datatable_buttons(self):
        if self.delete_last_measure_button.disabled:
            self.delete_last_measure_button.disabled = False
            self.empty_table_button.disabled = False
            self.delete_last_measure_button.style = self.button_style
            self.empty_table_button.style = self.button_style
        else:
            self.delete_last_measure_button.disabled = True
            self.empty_table_button.disabled = True
            self.delete_last_measure_button.style = self.disabled_button_style
            self.empty_table_button.style = self.disabled_button_style

    def set_mb_table(self, mb_table: ft.Container):
        self.mb_table = mb_table

    def delete_last_measure(self):
        is_empty = self.mb_table.delete_last_value()

        if is_empty:
            self.toggle_datatable_buttons()
            self.mb_table.set_placeholder()

        # BORRAR ULTIMA MEDICIÓN DEl NCL
        global ncl
        ncl.delete_last_measure()

    def empty_datatable(self):
        self.toggle_datatable_buttons()
        self.mb_table.set_placeholder()

        # BORRAR TODAS LAS MEDICIONES DEL NCL
        global ncl
        ncl.delete_all_measures()

    def reset_time_manager(self):
        self.reset_timer_dialog.open = True


class MeasuresBlock(ft.Container):
    def __init__(self):
        super().__init__(**section_block_invisible_style)
        self.content_height = 520
        self.height = self.content_height

        ## VENTANA EMERGENTE: Cambio de start_time
        def rtd_yes_action():
            time_manager.reset_start_time()
            # Vaciar tabla si no esta vacía
            if mb_table.placeholder_deleted:
                mb_options.empty_datatable()
            # ELIMINAR TODAS LAS MEDICIONES DEL NCL
            global ncl
            if ncl is not None:
                ncl.delete_all_measures()
            self.reset_timer_dialog.open = False

        def rtd_no_action():
            self.reset_timer_dialog.open = False

        self.reset_timer_dialog = ft.AlertDialog(
            modal=True,  # Obligatorio responder
            bgcolor=LIGHT_COLORS["background"],
            title=ft.Text(
                "Posible pérdida de datos",
                **TEXT_STYLES["alert_dialog_title_style"],
            ),
            content=ft.Text(
                "Reiniciar el tiempo de referencia del cronómetro borrará todas las mediciones que \n"
                + "utilizan tiempo relativo. Esto incluye todas las mediciones de temperatura que ha \n"
                + "guardado hasta el momento. ¿Desea proceder?",
                **TEXT_STYLES["alert_dialog_description_style"],
            ),
            actions=[
                ft.TextButton(
                    ft.Text(
                        "Sí, eliminar mediciones",
                        **TEXT_STYLES["alert_dialog_textbutton_style"],
                    ),
                    on_click=rtd_yes_action,
                ),
                ft.TextButton(
                    ft.Text(
                        "No, cancelar",
                        **TEXT_STYLES["alert_dialog_textbutton_style"],
                    ),
                    on_click=rtd_no_action,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,  # Alinea los botones a la derecha
        )

        ## VENTANA EMERGENTE: Error al ingresar medicion con ncl sin definir
        def nnd_ok_action():
            self.ncl_not_defined_dialog.open = False

        self.ncl_not_defined_dialog = ft.AlertDialog(
            modal=True,  # Obligatorio responder
            bgcolor=LIGHT_COLORS["background"],
            title=ft.Text(
                "Error",
                **TEXT_STYLES["alert_dialog_title_style"],
            ),
            content=ft.Text(
                "Por favor, defina los parámetros del módulo NCL antes de ingresar mediciones.",
                **TEXT_STYLES["alert_dialog_description_style"],
            ),
            actions=[
                ft.TextButton(
                    ft.Text(
                        "Aceptar",
                        **TEXT_STYLES["alert_dialog_textbutton_style"],
                    ),
                    on_click=nnd_ok_action,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,  # Alinea los botones a la derecha
        )

        ## SUBBLOQUE: Measures
        mb_measures = MeasuresBlock_Measures(self.ncl_not_defined_dialog)

        self.time_measure_field = mb_measures.time_measure_field
        self.temperature_measure_field = mb_measures.temperature_measure_field

        ## SUBBLOQUE: TimeNow
        mb_time_now = MeasuresBlock_TimeNow()

        self.time_text = mb_time_now.time_text
        self.r_time_text = mb_time_now.rtime_text
        self.r_time_since_text = mb_time_now.rtime_since_text

        ## SUBBLOQUE: Table
        mb_table = MeasuresBlock_Table()

        mb_measures.set_mb_table(mb_table)

        ## SUBBLOQUE: AmbientalConditions
        mb_ambiental_conditions = MeasuresBlock_AmbientalConditions()

        ## SUBBLOQUE: Options
        mb_options = MeasuresBlock_Options(self.reset_timer_dialog)

        mb_options.set_mb_table(mb_table)
        mb_table.set_mb_options(mb_options)

        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        mb_time_now,
                        mb_table,
                    ],
                    expand=True,
                ),
                ft.Row(
                    controls=[
                        mb_measures,
                        mb_ambiental_conditions,
                        mb_options,
                    ],
                    expand=True,
                ),
            ],
            # height=self.content_height,
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

    def load_labels(self):
        x_labels: list[ftc.ChartAxisLabel] = []
        y_labels: list[ftc.ChartAxisLabel] = []

        for i in range(0, 100):
            y_labels.append(
                ftc.ChartAxisLabel(
                    value=i,
                    label=ft.Text(
                        str(i),
                        **TEXT_STYLES["gav_chart_label_style"],
                    ),
                )
            )

        for i in range(int(self.min_x), int(self.max_x)):
            x_labels.append(
                ftc.ChartAxisLabel(
                    value=i,
                    label=ft.Text(
                        str(i),
                        **TEXT_STYLES["gav_chart_label_style"],
                    ),
                )
            )

        self.bottom_axis.labels = x_labels
        self.left_axis.labels = y_labels

    def create_data_point(self, x, y, line: int):
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

            self.line_1.points = self.points_1.copy()
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

            self.line_2.points = self.points_2.copy()
        self.update_axis_limits()
        self.load_labels()

    def set_tpoint_list_to_line(self, point_list: list[TPoint], line: int):
        # Borrar todo en la línea
        if line == 1:
            self.points_1 = []
            self.line_1.points = []
        if line == 2:
            self.points_2 = []
            self.line_2.points = []

        # Añadir puntos a la línea
        for i in range(0, len(point_list)):
            x = point_list[i].rtime
            y = point_list[i].temperature
            self.create_data_point(x, y, line)


class GraphAndValuesBlock_Graph(ft.Container):
    def __init__(self):
        super().__init__(**section_block_style)
        self.padding = ft.Padding(10, 30, 30, 10)
        self.expand = 3

        self.graph = GAVChart(BASE_COLORS["color_3"], BASE_COLORS["color_4"])

        self.content = self.graph

        self.set_placeholder()

    def set_placeholder(self):
        placeholder_values_1: list[TPoint] = []
        placeholder_values_2: list[TPoint] = []

        for i in range(0, 30):
            example_temp_1 = 50 * math.exp(-0.2 * i) + 3 * random.random()
            placeholder_values_1.append(TPoint(i, example_temp_1))

            example_temp_2 = 50 * math.exp(-0.2 * i) + 3 * random.random()
            placeholder_values_2.append(TPoint(i, example_temp_2))

        self.graph.set_tpoint_list_to_line(placeholder_values_1, 1)
        self.graph.set_tpoint_list_to_line(placeholder_values_2, 2)


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

        self.content_height = 400
        self.height = self.content_height

        self.graph_block = GraphAndValuesBlock_Graph()
        self.predicted_block = GraphAndValuesBlock_Predicted()

        self.content = ft.Row(
            controls=[
                self.graph_block,
                self.predicted_block,
            ],
            height=self.content_height,
            expand=True,
        )

    def update_graph(self):
        global ncl
        if ncl is not None:
            if ncl.is_ready():
                ## OBTENER ARRAY DE RESULTADOS (CON METODO ANALÍTICO)
                raw_func_array = ncl.get_prediction_with_function(10)
                func_array = []
                for i in range(0, len(raw_func_array) // 8):
                    func_array.append(raw_func_array[i * 8])

                ## OBTENER ARRAY DE RESULTADOS (CON METODO DE EULER)
                raw_euler_array = ncl.get_prediction_with_euler(10)
                euler_array = []
                for i in range(0, len(raw_euler_array) // 8):
                    euler_array.append(raw_euler_array[i * 8])

                ## FIJAR ARRAYS A LA GRAFICA
                self.graph_block.graph.set_tpoint_list_to_line(func_array, 1)
                self.graph_block.graph.set_tpoint_list_to_line(euler_array, 2)

                # DEBUG
                if debug_options["show_ncl_returned_func_values"]:
                    print(
                        "<GraphAndValuesBlock> update_graph() -> RETURNED FUNC ARRAY (AFTER CROPPING)"
                    )
                    for i in range(0, len(func_array)):
                        print(f"index {i}. \t\t {func_array[i]}")

                if debug_options["show_ncl_returned_euler_values"]:
                    print(
                        "<GraphAndValuesBlock> update_graph() -> RETURNED EULER ARRAY (AFTER CROPPING)"
                    )
                    for i in range(0, len(euler_array)):
                        print(f"index {i}. \t\t {euler_array[i]}")
            else:
                print(
                    "<GraphAndValuesBlock> update_graph() -> could not get array because NCL IS NOT READY"
                )
        else:
            print(
                "<GraphAndValuesBlock> update_graph() -> could not get array because NCL IS NOT DEFINED"
            )


# BLOQUE DE OPCIONES AVANZADAS _________________________________________________
# Contiene un panel de opciones que permiten habilitar ciertas herramientas
# con propósitos de desarrollo y testeo.


class DebugBlock(ft.Container):
    def __init__(self):
        super().__init__(**section_block_style)

        global debug_options
        self.content_height = 250
        self.height = self.content_height

        self.chk_show_relative_time_field = ft.Checkbox(
            ft.Text(
                "Permitir ingresar tiempos relativos",
                **TEXT_STYLES["checkbox_label_style"],
            ),
            on_change=self.on_change_show_relative_time_field,
            value=True,
            **checkbox_style,
        )

        self.chk_show_temp_manager_values = ft.Checkbox(
            ft.Text(
                "Mostrar en la consola los valores del TimeManager",
                **TEXT_STYLES["checkbox_label_style"],
            ),
            on_change=self.on_change_show_temp_manager_values,
            **checkbox_style,
        )

        self.chk_show_ncl_returned_func_values = ft.Checkbox(
            ft.Text(
                "Mostrar en la consola el listado de valores calculados del MÉTODO ANALÍTICO",
                **TEXT_STYLES["checkbox_label_style"],
            ),
            on_change=self.on_change_show_ncl_returned_func_values,
            **checkbox_style,
        )

        self.chk_show_ncl_returned_euler_values = ft.Checkbox(
            ft.Text(
                "Mostrar en la consola el listado de valores calculados del MÉTODO DE EULER",
                **TEXT_STYLES["checkbox_label_style"],
            ),
            on_change=self.on_change_show_ncl_returned_euler_values,
            **checkbox_style,
        )

        self.content = ft.Column(
            controls=[
                ft.Text(
                    "Opciones Avanzadas (De Prueba)", **TEXT_STYLES["title_3_style"]
                ),
                self.chk_show_relative_time_field,
                self.chk_show_temp_manager_values,
                self.chk_show_ncl_returned_func_values,
                self.chk_show_ncl_returned_euler_values,
            ],
            expand=True,
        )

    def on_change_show_relative_time_field(self):
        global debug_options
        debug_options["show_relative_time_field"] = (
            self.chk_show_relative_time_field.value
        )

        print(
            f"<DebugBlock> CHANGED DEBUG CONFIG: 'show_relative_time_field' -> {self.chk_show_relative_time_field.value}"
        )  # Debug

    def on_change_show_temp_manager_values(self):
        global debug_options
        debug_options["show_temp_manager_values"] = (
            self.chk_show_temp_manager_values.value
        )

        print(
            f"<DebugBlock> CHANGED DEBUG CONFIG: 'show_temp_manager_values' -> {self.chk_show_temp_manager_values.value}"
        )  # Debug

    def on_change_show_ncl_returned_func_values(self):
        global debug_options
        debug_options["show_ncl_returned_func_values"] = (
            self.chk_show_ncl_returned_func_values.value
        )

        print(
            f"<DebugBlock> CHANGED DEBUG CONFIG: 'show_ncl_returned_func_values' -> {self.chk_show_ncl_returned_func_values.value}"
        )  # Debug

    def on_change_show_ncl_returned_euler_values(self):
        global debug_options
        debug_options["show_ncl_returned_euler_values"] = (
            self.chk_show_ncl_returned_euler_values.value
        )

        print(
            f"<DebugBlock> CHANGED DEBUG CONFIG: 'show_ncl_returned_euler_values' -> {self.chk_show_ncl_returned_euler_values.value}"
        )  # Debug


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


# VIEW PRINCIPAL _______________________________________________________________
# Este es el lugar donde toda la página se ensambla. Debido a limitaciones del
# propio flet, la verdadera Page se encuentra en el módulo `main.py`. Este view
# agrupa todos los componentes y sus layouts para que `main.py` las muestre
# correctamente y las maneje según los botones que presione el usuario.


def view(page: ft.Page):

    # DICCIONARIO DE FLAGS PARA OPCIONES DE DESARROLLADOR ______________________
    # Es un diccionario temporal que guarda las configuraciones del usuario

    global debug_options
    debug_options = {
        "show_relative_time_field": True,
        "show_temp_manager_values": False,
        "show_ncl_returned_func_values": False,
        "show_ncl_returned_euler_values": False,
    }

    # MÓDULOS DE CÁLCULO _______________________________________________________
    # En esta sección se encuentran los componentes necesarios para los cálculos
    # del tiempo y otros.

    global time_manager
    time_manager = TimeManager(3)
    global ncl
    ncl = None
    global ncl_update_intervals
    ncl_update_intervals = None

    # COLUMNA CENTRAL __________________________________________________________
    # Todos los componentes de la página se colocan dentro de una columna
    # envuelta en un container que restringe su tamaño al 80% horizontal.

    block_1 = NCLConfigBlock()
    block_2 = MeasuresBlock()
    block_3 = GraphAndValuesBlock()
    block_4 = DebugBlock()
    block_5 = MoreInfoBlock(page)

    # VENTANAS EMERGENTES PRECARGADAS __________________________________________
    # Estas son ventanas emergentes que deben ser precargadas para poder ser
    # luego mostradas.

    page.add(block_1.permanent_ncl_dialog)
    page.add(block_2.reset_timer_dialog)
    page.add(block_2.ncl_not_defined_dialog)

    central_column = ft.Container(
        content=ft.Column(
            controls=[
                TitleBlock(),
                SectionTitle("Configuración de Predicciones", block_1),
                block_1,
                SectionTitle("Mediciones de Temperatura", block_2),
                block_2,
                SectionTitle("Gráficas y Valores Calculados", block_3),
                block_3,
                SectionTitle("Debug", block_4),
                block_4,
                block_5,
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

    # FUNCIÓN DE ACTUALIZACIÓN _____________________________________________________
    # Esta función es la que se encarga de actualizar los componentes cada segundo
    # o en intervalos de tiempo incluso más cortos.

    async def async_update():
        page.update()

    global tick_count
    tick_count = -1

    def tm_runnable_tick():
        global tick_count
        global ncl_update_intervals
        tick_count += 1
        if tick_count >= 1000000:
            tick_count = 0
            print(
                "<tm_runnable_tick> Warning: tick_count exceeded 1,000,000! Reset to 0."
            )
        if ncl_update_intervals is not None:
            if tick_count >= ncl_update_intervals:
                tick_count = 0
                print(f"<tm_runnable_tick> tick_count = {tick_count} | Reset to 0.")

                block_3.update_graph()

        # BLOQUE 1: MeasuresBlock()
        if ncl is not None:
            time_now = time_manager.format_relative_time(
                time_manager.get_relative_time(), 5
            )
            block_2.time_text.value = time_now

            rtime_now = f"{time_manager.get_relative_time():.1f} sec"
            block_2.r_time_text.value = rtime_now

            start_time = time_now = time_manager.format_relative_time(0, 5)
            block_2.r_time_since_text.value = f"desde las {start_time}"

        # BLOQUE 2: NCLConfigBlock()
        block_1.update_calculated_values()

        # BLOQUE 5: MoreInfoBlock()
        block_2.time_measure_field.visible = debug_options["show_relative_time_field"]

        # ACTUALIZACIÓN
        page.run_task(async_update)

        # DEBUG

        if debug_options["show_temp_manager_values"]:
            print(f"tick_count -> {tick_count}")
            print("get_time() -> ", time_manager.get_time())
            print("get_relative_time() -> ", time_manager.get_relative_time())
            print(
                "get_relative_time_to_timestamp(get_time()) -> ",
                time_manager.relative_time_to_timestamp(time_manager.get_time()),
            )
            print(
                "format_relative_time(get_relative_time()) -> ",
                time_manager.format_relative_time(time_manager.get_relative_time(), 5),
            )

    time_manager.set_runnable_tick(tm_runnable_tick)
    time_manager.start_runnable()

    return content
