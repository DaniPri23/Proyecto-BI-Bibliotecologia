# Evidencias de Ejecución y Auditoría

Esta carpeta contiene los entregables automáticos generados por el pipeline ETL como respaldo del procesamiento de los datos, así como capturas de pantalla de la auditoría.

## Contenido de la Carpeta

### Reportes y Logs
* **`etl_log_ejecucion.txt`**: Bitácora de ejecución del script de Python. Registra cada paso del proceso (extracción, transformación, carga y verificado) junto con marcas de tiempo (timestamps) y la cantidad de registros procesados por cada fuente y tabla del Data Warehouse.
* **`etl_resumen_transformaciones.csv`**: Tabla en formato CSV que documenta las 12 transformaciones clave ejecutadas en el código, facilitando su revisión rápida en Power BI u otros sistemas.
* **`etl_evidencia_clasificacion.csv`**: Archivo CSV con los 381 estudiantes de primer ingreso analizados. Contiene el cálculo final de cohorte, cursos de transición matriculados, cantidad de cursos pendientes, estado de actividad, escenario de transición asignado (1-4), indicador de aptitud para plan 2027 y la bandera de levantamiento de requisitos.

### Capturas de Control y Validación (Imágenes)
* **`evidencia_resultados_modelo.png`**: Imagen de control que muestra el éxito de la carga de las 7 tablas físicas del esquema estrella y la verificación del conteo de registros en SQLite.
* **`evidencia_distribucion_cohortes.png`**: Imagen que demuestra la auditoría de negocio ejecutada mediante SQL, mostrando las estadísticas agregadas de cohortes, distribución de escenarios de transición, y recuento de cursos pendientes.
