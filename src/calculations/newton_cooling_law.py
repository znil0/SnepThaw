# MÓDULO: Ley de Enfriamiento de Newton
# Este script de python contiene los métodos relacionados con la Ley de
# Enfriamiento de Newton, incluyendo aquellos que lo implementan y calculan
# numéricamente las temperaturas.

from .data_types import Medicion
from .num_methods import euler_method
import math as m


# MÉTODOS AUXILIARES
def edo_f(r, Tm):
    """Retorna una función lambda f de variables (t, T) con la Ley de
    Enfriamiento de Newton en la forma: dy/dt = f(t, y)"""
    return lambda t, T: (-1)*r*(T - Tm)



# MÉTODOS PRINCIPALES
## Sin métodos numéricos
def create_ncl_function(temp_1: Medicion, temp_2: Medicion, amb_temp: float):
    """Con base en 2 mediciones de temperatura consecutivas y la temperatura
    ambiente, retorna una función solución que modela el enfriamiento
    respecto al tiempo, según la Ley de Enfriamiento de Newton."""

    r = (1/temp_2.tiempo)*m.log((temp_1.temperatura - amb_temp)/(temp_2.temperatura - amb_temp))

    return lambda t: amb_temp + (temp_1.temperatura - amb_temp)*m.exp((-1)*r*(t - temp_1.tiempo))



## Con métodos numéricos (Método de Euler)
def estimate_ncl_from_edo(temp_1: Medicion, temp_2: Medicion, amb_temp: float, tf:int, step:float):
    """Con base en 2 mediciones de temperatura consecutivas y la temperatura
    ambiente, retorna dos arrays. Donde el primero es un array de tiempos
    que empieza en temp_1.tiempo, termina en tf, y el segundo es un array
    de temperaturas aproximadas conseguidas mediante el método de Euler."""

    r = (1/temp_2.tiempo)*m.log((temp_1.temperatura - amb_temp)/(temp_2.temperatura - amb_temp))

    tiempos, temperaturas = euler_method(edo_f(r, amb_temp), 
                                         temp_1.temperatura, 
                                         temp_1.tiempo, 
                                         tf,
                                         step)
    return tiempos, temperaturas