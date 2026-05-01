# MÓDULO: Gestor de tiempo
# Resulta que manejar tiempo en python es un martirio (y en cualquier
# lenguaje en realidad). Así que esta librería tiene como objetivo
# manejar y estandarizar la manera en la que el programa maneja el tiempo.
# No estoy seguro que los métodos se vayan a comportar bien si le doy
# valores demasiado grandes, así que uso tiempo relativos desde la
# instanciación de la clase.


import time
import datetime as dt
from src.calculations.data_types import TempMeasure, TPoint


class TimeManager:
    def __init__(self, interval_exp: float):
        """Al instanciar `TimeManager`, se define la hora de instanciado como
        el segundo `0`. Y los tiempos relativos son los segundos después del
        mismo.

        `interval_exp`: limita la cantidad de decimales que se expresan
        a fracciones `2^interval_exp` de segundo. Un `interval_exp = 3`, hará
        que todos los tiempos se expresen en términos de `0.125` segundos
        (`12.25`, `12.375`, `12.5` pero nunca `12.41`)."""

        self.interval = 1 / (2**interval_exp)
        self.start_time = self.round_to_interval(time.time())

    def round_to_interval(self, value: float):
        """Redondea al múltiplo más cercano del intervalo."""
        return round(value / self.interval) * self.interval

    def get_time(self):
        return self.round_to_interval(time.time())

    def get_relative_time(self, timestamp: float = None):
        if timestamp is None:
            timestamp = time.time()
        return self.round_to_interval(timestamp - self.start_time)

    def relative_time_to_timestamp(
        self, relative_time: float, hour_format: bool = False
    ):
        """Transforma un tiempo relativo (tiempo desde self.start_time)
        a un timestamp."""
        return self.start_time + relative_time

    def format_relative_time(self, relative_time: float):
        """Aplica formato a un tiempo relativo: Si `start_time` es a las `12:45:01`
        y el `relative_time=6` retorna `12:45:07`, sin contar días."""
        td = dt.timedelta(seconds=self.relative_time_to_timestamp(relative_time))
        return self.format_timedelta_hms(td)

    def format_timedelta_hms(self, td):
        """
        Convierte `timedelta` a string `HH:MM:SS` (ignora los días).
        """
        total_seconds = int(td.total_seconds())
        hours = (total_seconds // 3600) % 24  # Solo horas dentro del día
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def toTPoint(self, time_measure: TempMeasure):
        rtime = self.get_relative_time(time_measure.timestamp)
        temperature = time_measure.temperature
        return TPoint(rtime, temperature)

    # FUNCIONES PARA DEBUGGING
    def print_values(self):
        print("\nTIME MANAGER")
        print("self.start_time         -> ", self.start_time)
        print("self.start_time (td)    -> ", dt.timedelta(seconds=self.start_time))
