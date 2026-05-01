import flet as ft


# --- 1. Función para el Degradado ---
def get_unified_gradient():
    return ft.LinearGradient(
        begin=ft.Alignment(-1, -1),
        end=ft.Alignment(1, 1),
        colors=["white", "white", "#fff9c4"],
    )


# --- 2. Función para las targetas Verticales ---
def create_modern_card(title, description, on_click_destination):
    return ft.Container(
        content=ft.Column(
            [
                ft.Column(
                    [
                        ft.Text(
                            title,
                            size=26,
                            weight="bold",
                            color="#b71c1c",
                            text_align="center",
                        ),
                        ft.Container(height=10),
                        ft.Text(
                            description,
                            size=16,
                            color="#424242",
                            text_align="center",
                        ),
                    ],
                    horizontal_alignment="center",
                ),
                ft.Container(expand=True),
                ft.ElevatedButton(
                    content=ft.Text("Ir", color="white", size=18),
                    bgcolor="#b71c1c",
                    width=140,
                    height=50,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=12),
                    ),
                    on_click=lambda _: on_click_destination(),
                ),
            ],
            horizontal_alignment="center",
        ),
        width=300,
        height=450,
        bgcolor="white",
        border_radius=30,
        padding=ft.padding.all(35),
        shadow=ft.BoxShadow(
            blur_radius=20,
            color="#15000000",
            offset=ft.Offset(0, 10),
        ),
        border=ft.Border.all(1, "#f5f5f5"),
    )


# --- Función para las targetas horizontales (Las que se usan en la parte de miembros del equipo) ---
def create_staff_card(name, description):
    return ft.Container(
        content=ft.Column(
            [
                ft.Text(name, size=24, weight="bold", color="#b71c1c"),
                ft.Text(description, size=16, color="#424242", italic=False),
            ],
            alignment="center",
            spacing=5,
        ),
        width=800,
        height=100,
        bgcolor="white",
        border_radius=15,
        padding=ft.padding.only(left=40, right=40),
        alignment=ft.Alignment(-1, 0),
        shadow=ft.BoxShadow(
            blur_radius=15,
            color="#10000000",
            offset=ft.Offset(0, 5),
        ),
        border=ft.Border.all(1, "#f0f0f0"),
    )


# Ajustes para la grafica y donde se aran las opereaciones
# --- Estilos ---
in_style: dict = {
    "expand": 1,
    "bgcolor": "white",
    "border_radius": 15,
    "shadow": ft.BoxShadow(
        blur_radius=15,
        color="#15000000",
        offset=ft.Offset(0, 5),
    ),
    "border": ft.Border.all(1, "#f5f5f5"),
}

tracker_style: dict = {
    "main": {
        "expand": True,
        "bgcolor": "white",
        "border_radius": 15,
        "shadow": ft.BoxShadow(
            blur_radius=15,
            color="#15000000",
            offset=ft.Offset(0, 5),
        ),
        "border": ft.Border.all(1, "#f5f5f5"),
    }
}


# --- 2. Clases Minimalistas (Mismo comportamiento) ---
class GraphIn(ft.Container):
    def __init__(self):
        super().__init__(**in_style)


class GraphOut(ft.Container):
    def __init__(self):
        super().__init__(**in_style)


class Tracker(ft.Container):
    def __init__(self):
        super().__init__(**tracker_style.get("main"))


# --- Pantalla Principal ---
def primera_pantalla(page: ft.Page):
    page.controls.clear()
    background_gradient = ft.Container(expand=True, gradient=get_unified_gradient())

    image_layer = ft.Container(
        content=ft.Image(
            src="Recursos/prueba.png", width=450, height=450, fit="contain"
        ),
        alignment=ft.Alignment(1, 0),
        padding=ft.padding.only(right=80),
    )

    text_content = ft.Container(
        expand=True,
        padding=ft.padding.only(left=80),
        content=ft.Column(
            [
                ft.Text(
                    "HEAT-CALICO",
                    color="#b71c1c",
                    size=55,
                    weight="bold",
                    font_family="Arial Black",
                ),
                ft.Container(height=10),
                ft.ElevatedButton(
                    content=ft.Text("Inicio", color="white", size=22),
                    bgcolor="#424242",
                    width=240,
                    height=65,
                    elevation=8,
                    on_click=lambda e: segunda_pantalla(page),
                ),
            ],
            alignment="center",
            horizontal_alignment="start",
        ),
    )

    page.add(ft.Stack([background_gradient, image_layer, text_content], expand=True))
    page.update()


# --- Segunda Pantalla ---
def segunda_pantalla(page: ft.Page):
    page.controls.clear()
    background_gradient = ft.Container(expand=True, gradient=get_unified_gradient())

    layout_principal = ft.Column(
        [
            ft.Container(
                content=ft.Text(
                    "Segunda Pantalla", color="black", size=35, weight="bold"
                ),
                padding=ft.padding.only(top=50),
            ),
            ft.Row(
                [
                    create_modern_card(
                        "Operación",
                        "Visualiza y analiza los datos de el cambio de temperatura del objeto en tiempo real.",
                        lambda: tercera_pantalla(page),
                    ),
                    ft.Container(width=40),
                    create_modern_card(
                        "Staff",
                        "Información detallada sobre el equipo y los desarrolladores de este proyecto.",
                        lambda: cuarta_pantalla(page),
                    ),
                ],
                alignment="center",
            ),
            ft.Container(
                content=ft.ElevatedButton(
                    content=ft.Text("Volver", color="white"),
                    bgcolor="#424242",
                    width=160,
                    height=50,
                    on_click=lambda _: primera_pantalla(page),
                ),
                padding=ft.padding.only(bottom=50),
            ),
        ],
        alignment="space_between",
        horizontal_alignment="center",
        expand=True,
    )

    page.add(ft.Stack([background_gradient, layout_principal], expand=True))
    page.update()


# --- Funciones de navegación básicas para que el código corra ---
def tercera_pantalla(page: ft.Page):
    page.controls.clear()

    # Reutilizamos el gradiente de fondo (puedes llamar a tu función aquí)
    background_gradient = ft.Container(expand=True, gradient=get_unified_gradient())

    # Instanciamos tus clases limpias
    graph_in = GraphIn()  # Cuadro Grande de la Izquierda
    graph_out = GraphOut()  # Cuadro de Arriba Derecha
    tracker = Tracker()  # Cuadro de Abajo Derecha

    # --- NUEVA ESTRUCTURA DE MATRIZ (Copiando la foto) ---
    layout_operacion = ft.Container(
        expand=True,
        padding=20,
        content=ft.Column(
            [
                # Título y botón volver (Fila superior sutil)
                ft.Row(
                    [
                        ft.Text(
                            "Operacion Enfriamiento",
                            size=26,
                            weight="bold",
                            color="#b71c1c",
                        ),
                        ft.ElevatedButton(
                            "Volver", on_click=lambda _: segunda_pantalla(page)
                        ),
                    ],
                    alignment="spaceBetween",
                ),
                # Espacio entre el título y las cajas
                ft.Container(height=10),
                # --- EL CUERPO PRINCIPAL (Layout de la foto) ---
                ft.Row(
                    [
                        # Mitad IZQUIERDA: Cuadro Grande (GraphIn)
                        # Al estar en un Row con expand=True, ocupa el 50% de ancho
                        ft.Container(content=graph_in, expand=True),
                        # Mitad DERECHA: Columna con los otros dos
                        ft.Column(
                            [
                                # Fila superior derecha (GraphOut)
                                ft.Container(content=graph_out, expand=True),
                                # Fila inferior derecha (Tracker)
                                ft.Container(content=tracker, expand=True),
                            ],
                            expand=True,
                            spacing=20,  # Espacio vertical entre los dos cuadros derechos
                        ),
                    ],
                    expand=True,  # Hace que la fila use todo el alto disponible
                    spacing=20,  # Espacio horizontal entre la izquierda y la derecha
                ),
            ],
            spacing=0,  # Sin espacio extra entre el título y la matriz
        ),
    )

    page.add(ft.Stack([background_gradient, layout_operacion], expand=True))
    page.update()


# --- Cuarta Pantalla (Staff) ---
def cuarta_pantalla(page: ft.Page):
    page.controls.clear()
    background_gradient = ft.Container(expand=True, gradient=get_unified_gradient())

    titulo = ft.Container(
        content=ft.Text("Nuestro Equipo", color="black", size=40, weight="bold"),
        padding=ft.padding.only(top=50, bottom=20),
    )

    # Lista de Rectángulos Apilados
    staff_list = ft.Column(
        [
            create_staff_card("Leo", "ID: 24400863"),
            create_staff_card("Yabet", "A"),
            create_staff_card("Gerardo", "Nose"),
            create_staff_card("Hugo", "Pijas"),
        ],
        horizontal_alignment="center",
        spacing=15,
    )

    boton_volver = ft.Container(
        content=ft.ElevatedButton(
            "Volver al Menú",
            bgcolor="#424242",
            color="white",
            width=200,
            height=50,
            on_click=lambda _: segunda_pantalla(page),
        ),
        padding=ft.padding.only(bottom=50),
    )

    layout_final = ft.Column(
        [
            titulo,
            ft.Container(height=10),
            staff_list,
            ft.Container(expand=True),  # Empuja el botón al fondo
            boton_volver,
        ],
        horizontal_alignment="center",
        expand=True,
    )

    page.add(ft.Stack([background_gradient, layout_final], expand=True))
    page.update()


# --- Función de Entrada ---
def main(page: ft.Page):
    page.title = "Heat-Calico"
    page.padding = 0
    page.window_width = 1100
    page.window_height = 850
    primera_pantalla(page)
