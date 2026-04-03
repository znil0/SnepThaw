# MÓDULO: Tipos de Datos
# Este script de python contiene los tipos de datos que utilizan los demás
# módulos y otros métodos auxiliares relacionados a ellos.

from collections import namedtuple

# Tipos de dato
Medicion = namedtuple('Medicion', ['tiempo', 'temperatura'])