import flet as ft
from src.ui.constants.theme_colors import LIGHT_COLORS


TEXT_STYLES: dict = {
    ## PARA TÍTULOS DE CADA PÁGINA
    "page_title_style": {
        "font_family": "Archivo",
        "size": 24,
        "weight": "w400",
        "color": LIGHT_COLORS["primary"],
    },
    ## PARA LAS DESCRIPCIONES PEQUEÑAS DE CADA PÁGINA
    "page_description_style": {
        "font_family": "DM Sans 14pt",
        "size": 14,
        "weight": "w300",
        "color": ft.Colors.with_opacity(0.8, LIGHT_COLORS["text"]),
    },
    ## PARA LOS BREADCRUMBS DE LAS PÁGINAS
    "breadcrumb_secondary_style": {
        "font_family": "DM Sans 14pt",
        "size": 12,
        "weight": "w300",
        "color": LIGHT_COLORS["text"],
    },
    "breadcrumb_primary_style": {
        "font_family": "DM Sans 14pt",
        "size": 12,
        "weight": "w400",
        "color": LIGHT_COLORS["primary"],
    },
    ## PARA TITULO GENERICO SUPERIOR (TAMAÑO 1)
    "suptitle_1_style": {
        "font_family": "DM Sans 14pt",
        "size": 16,
        "weight": "w300",
        "color": LIGHT_COLORS["text"],
    },
    ## PARA TITULO GENERICO (TAMAÑO 1)
    "title_1_style": {
        "font_family": "Archivo",
        "size": 24,
        "weight": "w300",
        "color": LIGHT_COLORS["primary"],
    },
    ## PARA TITULO DE SUBSECCION (TAMAÑO 3)
    "title_3_style": {
        "font_family": "Archivo",
        "size": 16,
        "weight": "w400",
        "color": LIGHT_COLORS["primary"],
    },
    ## PARA TÍTULOS (DIVISORES) DE LAS SECCIONES DE CADA PÁGINA
    "section_title_style": {
        "font_family": "Archivo",
        "size": 14,
        "weight": "w400",
        "color": ft.Colors.with_opacity(0.5, LIGHT_COLORS["text"]),
    },
    "section_divider_style": {
        "color": ft.Colors.with_opacity(0.5, LIGHT_COLORS["text"]),
        "thickness": 1,
        "expand": True,
    },
    "section_divider_icon_style": {
        "width": 30,
        "height": 30,
        "icon": ft.Icons.EXPAND_LESS,
        "color": ft.Colors.with_opacity(0.5, LIGHT_COLORS["text"]),
    },
    ## PARA LOS ESPACIOS PARA ESCRIBIR LAS MEDICIONES DE TEMPERATURA
    "measure_text_field_style": {
        "font_family": "JetBrains Mono",
        "size": 14,
        "weight": "w600",
        "color": LIGHT_COLORS["text"],
    },
    "measure_text_field_label_style": {
        "font_family": "DM Sans 14pt",
        "size": 14,
        "weight": "w400",
        "color": LIGHT_COLORS["text"],
    },
    ## PARA LOS BOTONES DE ENVIAR
    "submit_button_text_style": {
        "font_family": "DM Sans 14pt",
        "size": 14,
        "weight": "w400",
        "color": LIGHT_COLORS["text"],
    },
    ## PARA LOS LABEL DE LAS TABLAS DE DATOS
    "table_label_style": {
        "font_family": "Archivo",
        "size": 14,
        "weight": "w400",
        "color": LIGHT_COLORS["primary"],
    },
    ## PARA LOS LABEL DE LAS TABLAS DE DATOS
    "table_values_style": {
        "font_family": "DM Sans 14pt",
        "size": 14,
        "weight": "w400",
        "color": LIGHT_COLORS["text"],
    },
    ## PARA DATOS GRANDES
    "big_value_1_style": {
        "font_family": "Archivo",
        "size": 42,
        "weight": "w500",
        "color": LIGHT_COLORS["primary"],
    },
    "big_value_2_style": {
        "font_family": "Archivo",
        "size": 36,
        "weight": "w500",
        "color": LIGHT_COLORS["primary"],
    },
    "checkbox_label_style": {
        "font_family": "DM Sans 14pt",
        "size": 14,
        "weight": "w400",
        "color": LIGHT_COLORS["text"],
    },
    ## PARA NOTAS BREVES DE LOS COMPONENTES
    "small_note_style": {
        "font_family": "DM Sans 14pt",
        "size": 14,
        "weight": "w400",
        "color": LIGHT_COLORS["primary"],
    },
}
