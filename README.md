# SnepThaw
Un proyecto para una materia de Métodos Numéricos :P.

$$\Large \frac{\partial u}{\partial t} - \alpha \nabla^2 u = 0$$

## Integrantes del equipo
- La Muela 🦷
- El que no veía (pero yabe) 👁️
- Monitorman 🖥️
- Yo, uwu 🦁

## ¿Cuál es el plan?
Vamos a crear un programa en Python usando `Flet` (una librería parecida a Swing) para la interfaz y `numpy` si es posible. El objetivo es conseguir un programa que al teclear ciertos datos iniciales, pueda predecir el cambio de temperatura de un vaso con algún líquido.

Ya de por sí es problemático lidiar con fenómenos físicos porque dependen de muchos factores ambientales. Pero idealmente, usaremos dos planteamientos matemáticos distintos:

### Plan A: Ley de Enfriamiento de Newton
Con esta ley podemos predecir la manera en la que la temperatura de un cuerpo decrece al pasar el tiempo, asumiendo que la temperatura en el mismo se distribuya uniformemente sobre el mismo (lo cual suele ser el caso en líquidos muy conductores como el agua). Este es nuestro plan a prueba de errores, diseñado para que mi equipo no repruebe si me muero antes de que pueda terminar el otro planteamiento.

Básicamente es una ecuación diferencial lineal de primer orden (EDO)

$$\Large \frac{dT(t)}{dt} = -r(T - T_m)$$

que se resuelve trivialmente mediante separación de variables, quedando como

$$\Large T(t) = T_m + (T_0 - T_m)e^{-rt}\text{.}$$

Utiliza una cierta constante $r$ que representa el ritmo en el que se pierde calor, pero probablemente podamos estimarla tecleando dos mediciones de temperatura y comparando. *([este](https://es.wikipedia.org/wiki/Ley_del_enfriamiento_de_Newton) es el artículo en Wikipedia)*

Este método claramente no necesita de ningún método numérico, pues disponemos de la solución particular. Sin embargo, **para cumplir con el requerimento, utilizaremos el método de Euler,** que nos permite aproximar los valores de la solución partiendo de un valor inicial y dando saltos de longitud $h$ mediante la expresión

$$\Large y(t_{n+1}) \approx y(t_n) + hf(t_n, y(t_n))$$

que ya preparada queda como

$$\Large T(t_{n+1}) \approx T(t_n) - hr(T(t_n) - T_m)$$

donde solo tenemos que reemplazar $T_m$, comenzar con los valores iniciales $t_0$, $T(t_0)$ y fijar un salto $h$, para que los siguientes valores $t$ sean $t_{n+1} = t_n + h$. Es decir, si sabemos que en el segundo $t_0 = 1\text{s}$ la temperatura fue de $40\text{°C}$ entonces con un paso $h = 0.5\text{s}$ sabremos la temperatura en el segundo $t_1 = t_0 + 0.5 = 1.5\text{s}$.

Este método también se describe mejor en la justificación matemática.

### Plan B: Ecuación del Calor
Con esta ecuación diferencial parcial que parece sencilla a primera vista (pero es peor que un tumor en el qlo) podemos predecir la temperatura de un cuerpo **sólido** en cada uno de los puntos que lo conforman. La ecuación se plantea de forma genérica como

$$\Large \frac{\partial u}{\partial t} - \alpha \nabla^2 u = 0$$

donde la función $u(x_1, x_2, ..., x_n, t)$ representa la temperatura en un punto fijado por las coordenadas $x_n$ (que no necesariamente son cartesianas) y el tiempo $t$. El símbolo $\nabla^2$ representa el operador laplaciano que dependiendo de las coordenadas, se puede volver un verdadero infierno.

$$\Large \nabla^2 u = \frac{\partial^2 u}{\partial r^2} + \frac{1}{r}\frac{\partial u}{\partial r} + \frac{1}{r^2}\frac{\partial^2 u}{\partial \theta^2} + \frac{\partial ^2 u}{\partial z^2}$$

Evidentemente, usar la ecuación del calor en un vaso con agua es problemático por varias razones. Primero, la ecuación del calor asume que el objeto es sólido, es decir, que no se mueve. Solo considera el flujo de calor por conducción, ignorando la convección (que es propia de los líquidos con baja viscosidad). ***Por esa razón, este plan solo puede aplicarse en sustancias que sean espesas y que enfrien de forma desigual, como avena o alimentos poco líquidos.***

### Plan C: Ecuaciones de Navier-Stokes
Este plan es solo si nos queda tiempo. Las [ecuaciones de Navier-Stokes](https://es.wikipedia.org/wiki/Ecuaciones_de_Navier-Stokes) son las ecuaciones que modelan el flujo de calor por convección en un líquido. De conseguir manejarla, podremos simular el enfriamiento de toda clase de líquidos.

Si consigo terminar el desarrollo de la ecuación del calor, continuaremos con esta.

## ¿Por qué le cambiaste el nombre?
Porque Heat suena como a Celo, y pos me daba cosa. Poco más. Elegí SnepThaw porque Snep es abreviatura de Snow Leopard (jerga furra) y Thaw significa deshielar en inglés, esta vez me aseguré de que no hubieran interpretaciones siniestras del nombre. Ya no quiero poner nombres a nada por el resto de mi vida.
