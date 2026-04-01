# MÓDULO: Ley de Enfriamiento de Newton
# Este script de python contiene los métodos relacionados con la Ley de Enfriamiento
# de Newton, incluyendo aquellos que lo implementan y calculan numéricamente las temperaturas.

from data_types import Medicion
from num_methods import euler_method
import math as m


# Auxiliar
def edo_f(r, Tm):
    """Retorna la Ley de Enfriamiento de Newton en la forma: dy/dt = f(t, y)"""
    return lambda t, T: (-1)*r*(T - Tm)

# Sin métodos numéricos
def create_ncl_function(temp_1: Medicion, temp_2: Medicion, amb_temp: float):
    """Con base en 2 mediciones de temperatura consecutivas y la temperatura ambiente,
    retorna una función que modela el enfriamiento respecto al tiempo, según la Ley de
    Enfriamiento de Newton."""

    r = (1/temp_2.tiempo)*m.log((temp_1.temperatura - amb_temp)/(temp_2.temperatura - amb_temp))

    return lambda t: amb_temp + (temp_1.temperatura - amb_temp)*m.exp((-1)*r*(t - temp_1.tiempo))

# Con métodos numéricos (Método de Euler)
def estimate_ncl_from_edo(temp_1: Medicion, temp_2: Medicion, amb_temp: float, tf:int, step:float):
    r = (1/temp_2.tiempo)*m.log((temp_1.temperatura - amb_temp)/(temp_2.temperatura - amb_temp))
    t, y = euler_method(edo_f(r, amb_temp), temp_1.temperatura, temp_1.tiempo, tf, step)
    return t, y


