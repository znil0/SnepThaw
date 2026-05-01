from data_types import Medicion
import newton_module as nm
import matplotlib.pyplot as plt

m_inicial = Medicion(tiempo = 0, temperatura = 80.0)
m_control = Medicion(tiempo=60, temperatura=62.0)
temp_aire = 22.0
t_final = 200
h_paso = 1.0

t_euler, y_euler = nm.estimate_ncl_from_edo(m_inicial, m_control, temp_aire, t_final, h_paso)

# --- GENERACIÓN DE LA GRÁFICA ---

plt.figure(figsize=(10, 6))

# Graficamos la solución numérica de Euler
plt.plot(t_euler, y_euler, 
         color='#1F77B4', 
         linewidth=2.5, 
         label='Aproximación de Euler ($y_{next}$)',
         zorder=2)

# Marcadores para visualizar los pasos de integración (cada 20 unidades de tiempo)
plt.scatter(t_euler[::20], y_euler[::20], 
            color='#FF7F0E', 
            edgecolor='black',
            s=45, 
            label='Puntos de iteración',
            zorder=3)

# Configuración del lienzo (Estilo Ingeniería del Tec)
plt.title('Simulación de Enfriamiento Cilíndrico - Método de Euler', fontsize=14, fontweight='bold')
plt.xlabel('Tiempo ($s$)', fontsize=12)
plt.ylabel('Temperatura ($°C$)', fontsize=12)

# Línea de asíntota (Temperatura Ambiente)
plt.axhline(y=temp_aire, color='red', linestyle='--', alpha=0.6, 
            label=f'Temperatura Ambiente ({temp_aire}°C)')

plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(loc='upper right', frameon=True, shadow=True)

# Ajuste fino de los ejes
plt.xlim(0, t_final)
plt.ylim(temp_aire - 5, max(y_euler) + 10)

plt.tight_layout()
plt.show()