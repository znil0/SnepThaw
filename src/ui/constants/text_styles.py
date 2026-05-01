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
    ## PARA TITULO GENERICO SUPERIOR TAMAÑO 1
    "suptitle_1_style": {
        "font_family": "DM Sans 14pt",
        "size": 16,
        "weight": "w300",
        "color": LIGHT_COLORS["text"],
    },
    ## PARA TITULO GENERICO TAMAÑO 1
    "title_1_style": {
        "font_family": "Archivo",
        "size": 24,
        "weight": "w300",
        "color": LIGHT_COLORS["primary"],
    },
    ## PARA TÍTULOS DE LAS SECCIONES DE CADA PÁGINA
    "section_title_style": {
        "font_family": "Archivo",
        "size": 14,
        "weight": "w400",
        "color": LIGHT_COLORS["text"],
    },
    "section_divider_style": {
        "color": ft.Colors.with_opacity(0.5, LIGHT_COLORS["text"]),
        "thickness": 1,
        "expand": True,
    },
}
