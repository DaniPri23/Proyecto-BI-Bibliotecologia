# Proceso de Extracción, Transformación y Carga (ETL)

Esta carpeta contiene el código y la especificación de las transformaciones del pipeline de Business Intelligence.

## Contenido de la Carpeta

* **`02_etl_transicion_ebci.py`**: Script de Python que implementa el proceso ETL completo de forma automatizada e independiente de Power BI.
* **`04_Tabla_Transformaciones_ETL.xlsx`**: Matriz en Excel que contiene el inventario oficial de transformaciones documentadas con su campo origen, regla de negocio aplicada, comentarios y campo destino.

## Fases del Pipeline ETL

El script `02_etl_transicion_ebci.py` está modularizado en cuatro fases:

1. **Extracción (`extraer_datos()`):** Carga los datos de las 8 fuentes de entrada (archivos Excel y ODS de la carpeta `/data`) a memoria en DataFrames de pandas. Implementa motores específicos (`xlrd` para XLS antiguos, `openpyxl` para XLSX y `odf` para ODS).
2. **Transformación (`transformar_datos()`):** Aplica la lógica para resolver la transición curricular a través de transformaciones avanzadas, tales como:
   * Homologación de campos sensibles y limpieza.
   * Derivación de cohorte a través del prefijo del carné.
   * Clasificación de estudiantes en 4 escenarios de transición.
   * Cálculo de cursos de transición pendientes y requerimiento de levantamiento de requisitos.
   * Eliminación y anonimización de datos sensibles.
3. **Carga (`cargar_datos()`):** Crea la base de datos de SQLite vacía, ejecuta el script DDL para modelar el esquema estrella y realiza la carga masiva mediante `to_sql()` de pandas. Al final, ejecuta comprobaciones e imprime auditorías de negocio rápidas en consola.
4. **Evidencias (`generar_evidencias()`):** Escribe el log detallado del proceso en un archivo de texto, y genera resúmenes en archivos CSV que se guardan en la carpeta `/evidence`.

## Requisitos de Ejecución

Para ejecutar el ETL:
1. Abra una terminal en el directorio raíz del proyecto.
2. Ejecute el comando:
   ```bash
   python 02_etl_transicion_ebci.py
   ```
3. El proceso tardará menos de 3 segundos en completarse y generará los resultados en las carpetas correspondientes.
