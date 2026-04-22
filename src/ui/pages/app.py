## Aquí va la página principal que subirá el yabete de aquí.
## ESTA ES UNA PÁGINA VACÍA QUE SERÁ REEMPLAZADA POR LA PRINCIPAL.

import flet as ft
import main_screen as ms

def main(page: ft.Page):
    # Configuraciones básicas
    page.title = "Página Principal"
    page.bgcolor = ft.Colors.WHITE
    page.window.maximized = True
    ms.main_screen(page)
    
    page.update()

ft.app(target=main)