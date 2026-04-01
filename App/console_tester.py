# DEBUG: Tester de Consola
# Este script de python solo se usa para probar los resultados producidos por
# los demás módulos. No se usa en la aplicación principal.

import newton_module as nm
from data_types import Medicion




## LEY DE ENFRIAMIENTO DE NEWTON
## COMPARATIVA: VALOR REAL RESPECTO A MÉTODO DE EULER
# Ejemplo de uso (temperatura en 200 segundos, sabiendo lo siguiente:)
temp_1 = Medicion(10, 60) # 10s -> 60°C
temp_2 = Medicion(20, 50) # 20s -> 50°C
amb_temp = 20 # Ambiente a 20°C


temp_prediction_real = nm.create_ncl_function(temp_1, temp_2, amb_temp)
t, y = nm.estimate_ncl_from_edo(temp_1, temp_2, amb_temp, 200, 1)

euler_index = 0
for i in range(0, 200):
    print(f"{i}s \t {temp_prediction_real(i)}°C", end="\t\t")

    if (t[euler_index] == i):
        euler_index += 1
        print(f"{y[euler_index]}°C")
    else:
        print()

