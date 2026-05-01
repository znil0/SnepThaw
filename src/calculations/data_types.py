# MÓDULO: Tipos de Datos
# Este script de python contiene los tipos de datos que utilizan los demás
# módulos y otros métodos auxiliares relacionados a ellos.

from collections import namedtuple

# General

## TempMeasure: Medición con timestamp (desde el epoch) y temperatura °C
TempMeasure = namedtuple("TempMeasure", ["timestamp", "temperature"])

## TempPoint: Medición preparada para graficar.
## Tiempo relativo generado por TimeManager.
## Temperatura en °C
TPoint = namedtuple("TPoint", ["rtime", "temperature"])
