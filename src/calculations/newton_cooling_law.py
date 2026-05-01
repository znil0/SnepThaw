# MÓDULO: Ley de Enfriamiento de Newton
# Este script de python contiene los métodos relacionados con la Ley de
# Enfriamiento de Newton, incluyendo aquellos que lo implementan y calculan
# numéricamente las temperaturas.


from .data_types import TempMeasure, TPoint
from .num_methods import euler_method
from .time_manager import TimeManager
import math as m
import bisect


class NewtonCoolingLaw:
    def __init__(
        self,
        seconds_ahead: int,
        amb_temp: float = None,
        measure_1: TempMeasure = None,
        measure_2: TempMeasure = None,
        time_manager: TimeManager = None,
    ):
        """
        intervals_ahead: Cuantas predicciones va a retornar.
        amb_temp: Temperatura ambiente en °C.
        measure_1: Primera medición. (opcional, se pueden actualizar luego)
        measure_2: Segunda medición. (opcional, se pueden actualizar luego)
        time_manager: instancia de TimeManager. (Usar si se quiere proveer otra Hora Inicial o Intervalo)
        """

        self.amb_temp = amb_temp
        self.measure_1 = measure_1
        self.measure_2 = measure_2

        if time_manager is None:
            self.time_manager = TimeManager(2)
        else:
            self.time_manager = time_manager

        self.intervals_ahead = int(seconds_ahead / self.time_manager.interval)

        self.r = None
        if self.isReady():
            self.calculate_r()

    # MÉTODOS AUXILIARES
    def edo_f(self, r, Tm):
        """Retorna una función lambda f de variables (t, T) con la Ley de
        Enfriamiento de Newton en la forma: dT/dt = f(t, T)"""
        return lambda t, T: (-1) * r * (T - Tm)

    def isReady(self):
        """Función auxiliar que retorna True si todos los valores necesarios
        para los cálculos se encuentran correctamente capturados."""
        state = True

        if self.amb_temp is None:
            state = False
        elif self.measure_1 is None:
            state = False
        elif self.measure_2 is None:
            state = False

        return state

    def calculate_r(self):
        """Calcula la constante r que multiplica a la variable en las
        fórmulas de la Ley de Enfriamiento de Newton. Ver Justificación
        Matemática."""
        amb_temp = self.amb_temp
        time_1 = self.time_manager.get_relative_time(self.measure_1.timestamp)
        temp_1 = self.measure_1.temperature
        temp_2 = self.measure_2.temperature

        # Esta fórmula es exactamente la misma de la Justificación Matemática
        self.r = (1 / time_1) * m.log((temp_1 - amb_temp) / (temp_2 - amb_temp))

    def add_measure(self, temperature: float):
        """Método que añade una medición de temperatura, tomando el tiempo
        de ahora como referencia."""
        new_measure = TempMeasure(self.time_manager.get_time(), temperature)

        # Corrección: Si la medición 1 esta vacía, pero la medición 2 no lo está.
        # Mueve la medición 2 a la medición 1, y deja vacía medición 2.
        if self.measure_1 is None and self.measure_2 is not None:
            self.measure_1 = self.measure_2
            self.measure_2 = None

        # Caso 1: No hay ninguna medición.
        # Guarda la nueva medición en medición 1.
        if self.measure_1 is None and self.measure_2 is None:
            self.measure_1 = new_measure
            return

        # Caso 2: Hay una sola medición. (en medición 1)
        # Guarda la nueva medición en medición 2.
        if self.measure_1 is not None and self.measure_2 is None:
            self.measure_2 = new_measure
            if self.isReady():
                self.calculate_r()
            return

        # Caso 3: Hay dos mediciones guardadas, en medición 1 y 2.
        # Elimina la medición 1, mueve la medición 2 a medición 1, y
        # guarda la nueva medición en medición 2.
        if self.measure_1 is not None and self.measure_2 is not None:
            self.measure_1 = self.measure_2
            self.measure_2 = new_measure
            if self.isReady():
                self.calculate_r()
            return

    def add_amb_temp(self, temperature: float):
        self.amb_temp = temperature
        if self.isReady():
            self.calculate_r()

    ## Sin métodos numéricos
    def create_ncl_function(self):
        """Con base en 2 mediciones de temperatura consecutivas y la temperatura
        ambiente, retorna una función solución que modela el enfriamiento
        respecto al tiempo, según la Ley de Enfriamiento de Newton."""

        amb_temp = self.amb_temp
        time_1 = self.time_manager.get_relative_time(self.measure_1.timestamp)
        temp_1 = self.measure_1.temperature
        r = self.r

        return lambda t: amb_temp + (temp_1 - amb_temp) * m.exp((-1) * r * (t - time_1))

    ## Con métodos numéricos (Método de Euler)
    def estimate_ncl_from_edo(self, final_time: float, precision_exponent: int = 4):
        """Con base en 2 mediciones de temperatura consecutivas y la temperatura
        ambiente, retorna dos arrays. Donde el primero es un array de tiempos relativos
        que empieza en el tiempo relativo de measure_1 y termina en final_time,
        y el segundo es un array
        de temperaturas aproximadas conseguidas mediante el método de Euler."""

        amb_temp = self.amb_temp
        time_1 = self.time_manager.get_relative_time(self.measure_1.timestamp)
        temp_1 = self.measure_1.temperature
        r = self.r

        half_steps = 2**precision_exponent
        tiempos_relativos, temperaturas = euler_method(
            self.edo_f(r, amb_temp),
            temp_1,
            time_1,
            final_time,
            (self.time_manager.interval / half_steps),
        )

        ## Quitar los pasos intermediarios que aparecen al
        ## dar un precision_exponent mayor que 0.

        return tiempos_relativos[::half_steps], temperaturas[::half_steps]

    # MÉTODOS PRINCIPALES
    def get_prediction_with_function(self, before_now: int):
        """Método que retorna un array de `TPoint` usando la
        función solución de la EDO donde before_now es la cantidad de
        intervalos que se dejan de margen entre el primer tiempo y el
        tiempo que corresponde al tiempo de ahora."""

        time_now = self.time_manager.get_relative_time()
        start_time = time_now - self.time_manager.interval * before_now
        # end_time = start_time + self.intervals_ahead * self.time_manager.interval

        f = self.create_ncl_function()
        prediction = []
        for i in range(0, self.intervals_ahead):
            t = start_time + i * self.time_manager.interval
            prediction.append(
                TPoint(t, f(t))  # Tiempo Relativo , Temperatura
            )
        return prediction

    def get_prediction_with_euler(self, before_now: int, precision_exponent: int = 4):
        """Método que retorna un array de `TPoint` usando el
        método de Euler donde before_now es la cantidad de intervalos
        que se dejan de margen entre el primer tiempo y el tiempo que
        corresponde al tiempo de ahora."""

        time_now = self.time_manager.get_relative_time()
        start_time = time_now - self.time_manager.interval * before_now
        end_time = start_time + self.intervals_ahead * self.time_manager.interval

        X, Y = self.estimate_ncl_from_edo(end_time, precision_exponent)
        raw_prediction = [[x, y] for x, y in zip(X, Y)]

        ## Esta parte del código elimina los pasos que no son relevantes,
        ## es decir, todos los que tienen x menor que start_time.
        xs = [coord[0] for coord in raw_prediction]
        index = bisect.bisect_left(xs, start_time)
        prediction = raw_prediction[index:]

        ## Pasar a Lista de TPoints
        tpoint_prediction = []
        for point in prediction:
            tpoint_prediction.append(TPoint(point[0], point[1]))
        return tpoint_prediction

    # MÉTODOS PARA DEBUGGING
    def print_values(self):
        print("VALORES CAPTURADOS")
        print("self.intervals_ahead ->\t", self.intervals_ahead)
        print("self.amb_temp        ->\t", self.amb_temp)
        print("self.measure_1       ->\t", self.measure_1)
        print("self.measure_2       ->\t", self.measure_2)
        self.time_manager.print_values()

        print("VALORES CALCULADOS")
        print("self.isReady()       ->\t", self.isReady())
        print("self.r               ->\t", self.r)
