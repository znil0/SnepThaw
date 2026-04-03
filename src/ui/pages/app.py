## Aquí va la página principal que subirá el yabete de aquí.
## ESTA ES UNA PÁGINA VACÍA QUE SERÁ REEMPLAZADA POR LA PRINCIPAL.

import flet as ft

def main(page: ft.Page):
    # Configuraciones básicas
    page.title = "Página Principal"
    page.bgcolor = ft.Colors.WHITE
    page.window.width = 800
    page.window.height = 600
    
    page.update()

ft.app(target=main)