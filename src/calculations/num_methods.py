# MÓDULO: Métodos Numéricos
# Este script de python implementa métodos numéricos como el método de Euler
# y otros.



# MÉTODOS PRINCIPALES
def euler_method(f, y0, t0, tf, step):
    """
    Método de Euler para una EDO: dy/dt = f(t, y)
    
    Parámetros:
    f: función que define la EDO
    y0: condición inicial
    t0: tiempo inicial
    tf: tiempo final
    h: paso de integración
    
    Retorna:
    t: arreglo de tiempos
    y: arreglo de soluciones
    """
    n = int((tf - t0) / step) + 1
    t = [t0 + i * step for i in range(n)]
    y = [y0]
    
    for i in range(n - 1):
        y_next = y[i] + step * f(t[i], y[i])
        y.append(y_next)
    
    return t, y