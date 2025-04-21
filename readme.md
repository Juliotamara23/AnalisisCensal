# <h1 aling="center">Proyecto de Reportes y Análisis de Datos de Familias</h1>

Este proyecto en Python automatiza el procesamiento y la generación de reportes a partir de un archivo de Excel (`.xlsx`) que contiene información sobre el registro de familias. Permite identificar familias con múltiples miembros, jefes de familia registrados solos, advertencias en los registros y personas que se han registrado más de una vez. Los reportes se generan en formatos PDF, TXT y JSON.

## Funcionalidades

El proyecto realiza las siguientes tareas:

* **Procesamiento de Datos:** Lee y analiza un archivo XLSX, identificando la estructura familiar y posibles inconsistencias.
* **Reporte de Familias con Múltiples Miembros:** Genera un reporte que lista las familias con más de un miembro registrado.
* **Reporte de Jefes de Familia Solos:** Crea un reporte con los jefes de familia que se registraron como únicos miembros de su núcleo familiar.
* **Reporte de Advertencias:** Identifica y reporta posibles problemas en los registros, como personas sin un jefe de familia referenciado correctamente.
* **Reporte de Personas Repetidas:** Detecta y reporta las personas que aparecen más de una vez en el registro, basándose en su número de documento.
* **Generación de Reportes en Múltiples Formatos:** Los reportes se generan en archivos PDF, TXT y JSON para facilitar su visualización y uso en diferentes contextos.

## Estructura del Proyecto

El proyecto se organiza en los siguientes archivos:

* `Archivo/`: Directorio donde se espera encontrar el archivo de datos en formato XLSX (`Cuestionario Cabildo TATACHIO MIRABEL (Respuestas).xlsx` por defecto).
* `fonts/`: Directorio que contiene las fuentes necesarias para la generación de los reportes PDF (`DejaVuSans.ttf`, `DejaVuSans-Bold.ttf`).
* `reportes/`: Directorio raíz para los reportes generados.
    * `reportes/reportes_pdf/`: Contiene los reportes en formato PDF.
    * `reportes/reportes_txt/`: Contiene los reportes en formato TXT.
    * `reportes/reportes_json/`: Contiene los reportes en formato JSON.
* `procesamiento.py`: Contiene la lógica principal para leer, procesar y analizar los datos del archivo XLSX.
* `reportes_pdf.py`: Contiene la clase y la lógica para generar los reportes en formato PDF.
* `reportes_txt.py`: Contiene las funciones para generar los reportes en formato TXT.
* `reportes_json.py`: Contiene las funciones para generar los reportes en formato JSON.

## Requisitos

Para ejecutar este proyecto, necesitas tener instalado lo siguiente:

* **Python 3.13 o superior**
* Las siguientes librerías de Python:
    ```bash
    pip install pandas fpdf tabulate
    ```

## Configuración

Disclaimers:
* El archivo XLSX debe tener una estructura específica para que el procesamiento funcione correctamente. Asegúrate de que las columnas relevantes estén presentes y en el formato adecuado.
* Este archivo XLSX contiene datos sensibles que son parte de una encuesta. Por lo que no puedo compartirlo, sin embargo su estructura es la siguiente:

* **Cédula de jefe(a) de Familia:** Número de documento del jefe de familia.
* **Nombre:** Nombre completo de la persona (incluyendo primer y segundo nombre).
* **Apellido:** Apellido completo de la persona (incluyendo primer y segundo apellido).
* **DNI:** Número de documento de identidad (corresponde al campo 'Documento').
* **Parentesco:** Relación con el jefe de familia (ej. "Jefe", "Esposa", "Hijo", etc.).
* **Teléfono:** Número de teléfono de contacto.
* **Dirección:** Dirección del hogar.
* **Email:** Correo electrónico (este campo no estaba en la lista original, se añadió si está disponible en los datos).

Entre otros campos que varian según los datos pide el ministerio del interior de Colombia.

1.  **Clonar el repositorio.**
2.  **Crear los directorios necesarios:** Asegúrate de tener las carpetas `Archivo/`, `fonts/` y `reportes/reportes_pdf/`, `reportes/reportes_txt/`, `reportes/reportes_json/` creadas en la misma ubicación que los archivos `.py`.
3.  **Colocar el archivo de datos:** Coloca tu archivo de datos en formato XLSX dentro del directorio `Archivo/`. Por defecto, el script buscará un archivo llamado `Cuestionario Cabildo TATACHIO MIRABEL (Respuestas).xlsx`. Si tu archivo tiene un nombre diferente, deberás modificar la variable `ruta_archivo_xlsx` en los archivos de reporte (`reportes_pdf.py`, `reportes_txt.py`, `reportes_json.py`) para que coincida.
4.  **Incluir las fuentes:** Asegúrate de tener los archivos de fuente `DejaVuSans.ttf` y `DejaVuSans-Bold.ttf` dentro del directorio `fonts/`. Puedes descargar estas fuentes gratuitamente si no las tienes.

## Uso

Para generar los reportes, ejecuta los scripts de Python correspondientes:

* **Generar reportes en PDF:**
    ```bash
    python reportes_pdf.py
    ```
    Los archivos PDF se guardarán en la carpeta `reportes/reportes_pdf/`.

* **Generar reportes en TXT:**
    ```bash
    python reportes_txt.py
    ```
    Los archivos TXT se guardarán en la carpeta `reportes/reportes_txt/`.

* **Generar reportes en JSON:**
    ```bash
    python reportes_json.py
    ```
    Los archivos JSON se guardarán en la carpeta `reportes/reportes_json/`.

Al ejecutar cada script, se procesará el archivo XLSX y se generarán los reportes correspondientes en las carpetas designadas. Se mostrarán mensajes en la consola indicando la finalización y la ubicación de los archivos generados.

## Licencia

Este proyecto está bajo la licencia apache 2.0. Puedes usar, modificar y distribuir este código bajo los términos de la licencia.

## Contacto

Si tienes alguna pregunta o sugerencia sobre este proyecto, no dudes en contactar al autor.