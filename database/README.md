# Data Warehouse y Scripts de Base de Datos

Esta carpeta contiene el esquema estrella (modelo dimensional) de la base de datos de SQLite, la estructura del Data Warehouse y las consultas SQL de negocio.

## Contenido de la Carpeta

* **`01_ddl_modelo_dimensional.sql`**: Script DDL que define el esquema físico del Data Warehouse. Contiene la creación de 6 dimensiones y 1 tabla de hechos con sus respectivas claves primarias, foráneas e índices de rendimiento.
* **`03_consultas_verificacion.sql`**: Conjunto de 10 consultas SQL de negocio diseñadas para auditar e interrogar la base de datos y verificar los resultados de la transición curricular (cohortes, aptos, pendientes, activos, promedios).
* **`dw_transicion_ebci.db`**: Archivo de la base de datos SQLite resultante de la carga del pipeline ETL.

## Estructura del Modelo Dimensional (Esquema Estrella)

El modelo está optimizado para consultas analíticas y consta de las siguientes tablas:

### Dimensiones (Tablas DIM)
* **`DIM_ESTUDIANTE`**: Datos demográficos y académicos del estudiante (carné, nombre, sexo, cohorte, correo).
* **`DIM_CURSO`**: Cursos de los planes de estudio, con marcas específicas para identificar los cursos de transición.
* **`DIM_CARRERA`**: Detalles de los énfasis (BE y CI) y grados (Bachillerato y Licenciatura).
* **`DIM_TIEMPO`**: Períodos académicos representados de forma YYYYCC (ej. 202601 para I-2026).
* **`DIM_RECINTO`**: Información del campus de procedencia (Rodrigo Facio).
* **`DIM_ESTADO_TRANSICION`**: Combinaciones de estados académicos, tipo de matrícula y escenarios de transición.

### Tabla de Hechos (Fact Table)
* **`FACT_MATRICULA_ACADEMICA`**: Contiene las métricas y claves de enlace para el análisis cuantitativo de la matrícula de transición.
  * *Métricas:* `activo_matriculado`, `cursos_pendientes`, `apto_transicion`, `promedio_admision`.

## Instrucciones de Uso

Para ejecutar las consultas de verificación:
1. Abra un cliente compatible con SQLite (por ejemplo, **DB Browser for SQLite**).
2. Conéctese a la base de datos `dw_transicion_ebci.db`.
3. Abra y ejecute el archivo `03_consultas_verificacion.sql` para generar la auditoría de negocio en tiempo real.
