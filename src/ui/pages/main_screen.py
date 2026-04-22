import flet as ft
#import title_screen

def main_screen(page: ft.Page):
    page.controls.clear()
    page.bgcolor = "#F5F5F5"

    #2C3E50, B71C1C, FFFFFF
    PRINCIPAL_COLOR = "#2c3e50"
    TITLE_COLOR = "#B71C1C"
    TEXT_COLOR = "#FFFFFF"

    #--------------MENU-------------------------
    menu_layout = ft.Container(
        width = 250,
        bgcolor = PRINCIPAL_COLOR,
        padding = 30,
        content = ft.Column([
            ft.Text(
                value = "MENU",
                color = TEXT_COLOR,
                weight = "bold",
                size = 18
            ),
            ft.Divider(color = ft.Colors.WHITE_24),
            ft.Container(),
            ft.Text(
                value = "Inicio",
                color = TEXT_COLOR,
                size = 16
            ),
            
            ft.Text(
                value = "Newton",
                color = TEXT_COLOR,
                size = 16
            ),
            
            ft.Text(
                value = "Ecuación de calor",
                color = TEXT_COLOR,
                size = 16
            )
        ],
        spacing = 20
        )
    )

    #----------TITLE------------------------
    title_layout = ft.Container(
        content = ft.Text(
            value = "HeatCalico",
            color = TITLE_COLOR,
            size = 55,
            weight = "bold",
            font_family = "Arial Black"
        )
    )

    #------------------IMAGE-------------------------
    image_layout = ft.Container(
        expand = True,
        content = ft.Image(
            src = "assets/prueba.png",
            width = 450,
            height = 450,
            fit = "contain"
        )
    )

    #---------------------MEMBERS --------------------------------
    made_layout = ft.Container(
        expand = True,
        alignment = ft.Alignment.CENTER,
        content = ft.Column([
            ft.Text(
                value = "Integrantes",
                size = 22,
                weight = "bold",
                color = PRINCIPAL_COLOR,
                text_align = ft.TextAlign.CENTER
            ),

            ft.Text(
                value = """
                Chávez Andrade Hugo Lemuel
                Ramírez Nuñez Yabet Antonio
                Rojano Meza Leonardo Gael
                Ruíz Chávez Gerardo David
                """,
                size = 14,
                color = ft.Colors.GREY_800,
                text_align = ft.TextAlign.CENTER
            )
        ],
        horizontal_alignment = ft.CrossAxisAlignment.CENTER
        )
    )

    #------------------------- FINAL LAYOUT --------------------------------------
    final_layout = ft.Container(
        expand = True,
        content = ft.Row([
            menu_layout,
            ft.Container(
                expand = True,
                padding = 40,
                content = ft.Column([
                    title_layout,
                    ft.Row([
                        made_layout,
                        ft.Divider(height = 40, color = ft.Colors.TRANSPARENT),
                        image_layout
                    ]),
                ],
                scroll = ft.ScrollMode.AUTO,
                horizontal_alignment = ft.CrossAxisAlignment.CENTER
                )
            )
        ],
        spacing = 0,
        vertical_alignment = ft.CrossAxisAlignment.STRETCH
        )
    )

    page.add(final_layout)
    
    page.update()