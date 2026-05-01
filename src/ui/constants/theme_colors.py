# CONSTANTES: Colores del tema
# Oigaaaaaaaan, decidí un tema por mí mismo y soy super indeciso, no me digan
# "Ay se ve feito, cambiale los colores", así que decidí ponerlos en este
# script. Si los cambian, podran afectar a todas las páginas que los usan,
# así que ya no es necesario ir página por página cambiándolos.
# Si van a crear páginas, por favor importen los colores desde este script.

import flet as ft

BASE_COLORS = {
    "color_1": "#180161",
    "color_2": "#4F1787",
    "color_3": "#EB3678",
    "color_4": "#FB773C",
}

LIGHT_COLORS = {
    "text": "#06001a",  # color_1 darkened
    "background": "#fff7f2",  # otro, "#ffeee6",
    "primary": "#EB3678",
    "secondary": "#FB773C",
    "accent": "#180161",
}

LIGHT_COLORS_OLD = {
    "text": "#2b2d42",
    "background": "#edf2f4",
    "primary": "#d90429",
    "secondary": "#8d99ae",
    "accent": "#201f33",
    "cold": "#0f25f0",
}

DARK_COLORS = {
    "text": "#efefef",
    "background": "#101010",
    "primary": "#ff3a3f",
    "secondary": "#000000",
    "accent": "#ff8040",
    "cold": "#0080ff",
}
