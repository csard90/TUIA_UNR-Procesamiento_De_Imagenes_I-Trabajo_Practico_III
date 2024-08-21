# TUIA - TP1 Procesamiento de Imágenes I - TP3

## Problema 1 – Cinco dados

Las secuencias de video tirada_1.mp4, tirada_2.mp4, tirada_3.mp4 y tirada_4.mp4 corresponden a tiradas de 5 dados. Se debe realizar lo siguiente:

a) Desarrollar un algoritmo para detectar automáticamente cuando se detienen los dados y leer el número obtenido en cada uno. Informar todos los pasos de procesamiento.

b) Generar videos (uno para cada archivo) donde los dados, mientras estén en reposo, aparezcan resaltados con un bounding box de color azul y además, agregar sobre los mismos el número reconocido.


## Resolución

Este repositorio contiene un archivos de Python ("ejercicio_01.py") que se utilizan para la resolución de las consignas solicitadas en el Trabajo Práctico Nº 3. También contiene los videos requeridos para la ejecución y los resultados de la misma. 

### Abstract
Este script Python realiza el procesamiento de videos que capturan lanzamientos de dados sobre una superficie. Utiliza la biblioteca OpenCV para llevar a cabo tareas avanzadas de visión por computadora. El código comienza importando las bibliotecas necesarias y definiendo funciones clave para el procesamiento de imágenes, como la reconstrucción de imágenes y la eliminación de elementos en los bordes.

El proceso se estructura en un bucle principal que itera sobre varios videos predefinidos. Para cada video, el script configura la lectura del video original y la escritura del video procesado. Luego, realiza el procesamiento de cada frame del video, segmentando el paño y los dados mediante técnicas de procesamiento de imágenes y analizando la relación de aspecto y área de los componentes conectados. Se implementa un seguimiento de los dados y se detecta si están en movimiento o en reposo. El resultado final se presenta en cada frame con la superposición de los dados y sus respectivos números.


A continuación, se detallan los pasos para ejecutar este archivos en su entorno de desarrollo.

## Requisitos Previos

Antes de ejecutar los archivos, asegúrate de tener instalado Python en tu sistema. Puedes descargarlo desde [python.org](https://www.python.org/downloads/) e instalarlo siguiendo las instrucciones correspondientes a tu sistema operativo.

Además, es posible que necesites instalar algunas bibliotecas Python adicionales. Puedes hacerlo utilizando el administrador de paquetes `pip`. Ejecuta los siguientes comandos para instalar las bibliotecas necesarias (OpenCV - MathPlotLib - Numpy):

`pip install opencv-contrib-python matplotlib numpy`

## Ejecución del script

El archivo "ejercicio_01.py" realiza el procesamiento en serie de los cuatro videos de la consigna y genera los resultados solicitados. Para ejecutarlo, siga estos pasos:

* Asegúrese de que los videos a procesar estén en la misma carpeta que "ejercicio_01.py".
  
* Abra una terminal o línea de comandos en el directorio donde se encuentra "ejercicio_01.py".

* Ejecute el siguiente comando para ejecutar el script:
`python ejercicio_01.py`
  
El resultado del procesamiento de cada uno de los videos se mostrará en una ventana y se cerrará al finalizar. También se puede interrumpir el procesamiento de cada video presionando la tecla `q`.

La ejecución correcta del script generará la visualización de los cuatro videos (tirada_1.mp4, tirada_2.mp4, tirada_3.mp4 y tirada_4.mp4) y creará en el mismo directorio los videos con el procesamiento solicitado (resolucion_tirada_1.mp4, resolucion_tirada_2.mp4, resolucion_tirada_3.mp4 y resolucion_tirada_4.mp4).

## Advertencias

* Asegúrese de que los videos a procesar estén en el formato correcto y tengan el nombre adecuado según las instrucciones de cada archivo.

* Si encuentra problemas con las bibliotecas, asegúrese de que estén instaladas correctamente usando pip.
  
* Dentro del script se encuentra declarada una variable que hace referencia al directorio local en el que se encuentran los videos a procesar y en el que se guardarán los videos procesados con la extensión .mp4. 
