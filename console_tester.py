# DEBUG: Tester de Consola
# Este script de python solo se usa para probar los resultados producidos por
# los demás módulos. No se usa en la aplicación principal.

from src.calculations.data_types import Medicion
from src.calculations.newton_cooling_law import create_ncl_function, estimate_ncl_from_edo





def test_1_ley_de_enfriamiento_de_newton():
    """Test 1: LEY DE ENFRIAMIENTO DE NEWTON. Descripción:
    Queremos comparar el valor real con el aproximado por el método
    de Euler. create_ncl_function() es el valor real, mientras que
    estimate_ncl_from_edo() retorna aproximaciones en formato array."""
    
    # Ejemplo de uso: Queremos obtener temperatura en los siguientes
    # 200 segundos, sabiendo lo siguiente:

    temp_1 = Medicion(10, 60) # A los 10 segundos se midió 60°C
    temp_2 = Medicion(20, 50) # A los 20 segundos se midió 50°C
    amb_temp = 20 # Ambiente a 20°C


    temp_prediction_real = create_ncl_function(temp_1, temp_2, amb_temp)
    t, y = estimate_ncl_from_edo(temp_1, temp_2, amb_temp, 200, 1)

    euler_index = 0
    for i in range(0, 200):
        print(f"{i}s \t {temp_prediction_real(i)}°C", end="\t\t")

        if (t[euler_index] == i):
            euler_index += 1
            print(f"{y[euler_index]}°C")
        else:
            print()

