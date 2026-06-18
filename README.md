# Proyecto de Optimización - Modelo PLEM

Este repositorio contiene el código fuente y las instancias utilizadas para resolver el problema de localización de instalaciones capacitadas con flujo en dos niveles (Modelo PLEM).

## Equipo de Trabajo
* Matías Pajarito
* Sebastián Césped
* Felipe Morales
* Luckas Palma

## Estructura del Repositorio
* `instancias/`: Carpeta con los archivos de datos de prueba.
* `generador.py`: Script encargado de procesar o generar los datos iniciales.
* `solver_base.py`: Implementación principal del modelo matemático y algoritmo de resolución.
* `resultados_proyecto.csv`: Archivo con las salidas y costos obtenidos.

## Requisitos Previos
Para ejecutar este proyecto, necesitas tener Python 3.x instalado. Instala las dependencias necesarias ejecutando:

bash
pip install -r requirements.txt

## Instrucciones de Ejecución

    1. Primero, ejecuta el generador de instancias (si es necesario):
        "python generador.py"
    2. Luego, ejecuta el solver principal para encontrar la solución óptima:
        "python solver_base.py"