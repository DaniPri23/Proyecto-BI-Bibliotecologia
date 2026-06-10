# Fuentes de Datos Operacionales y de Soporte

Esta carpeta contiene todos los insumos de datos originales utilizados como entrada para el proceso de ETL.

## Contenido de la Carpeta

### Datos Operacionales (Insumos de Matrícula y Estudiantes)
* **`Lista_de_Estudiantes_Activos.xls`** (Formato `.xls` antiguo, procesado con `xlrd`): Contiene el padrón de 665 estudiantes de la EBCI registrados como activos académica y administrativamente.
* **`Lista_de_Estudiantes_Inactivos_1.xls`** (Formato `.xls` antiguo, procesado con `xlrd`): Contiene la base de datos de 2,227 estudiantes inactivos para su análisis de reincorporación.
* **`PRIMER_INGRESO_2024.xls`**, **`PRIMER_INGRESO_2025.xls`**, **`PRIMER_INGRESO_2026.xls`** (Formato `.xls` antiguo, procesados con `xlrd`): Registros históricos del total de estudiantes admitidos en la carrera por año para la derivación de cohortes.
* **`LISTAS_DE_CLASE_2026BI1001_BI1002_BI2006.ods`** (Formato OpenDocument `.ods`, procesado con `odfpy`): Registro de matrículas de los tres cursos de transición del I ciclo 2026.
* **`Población_estudiantil_Iciclo2026_Bach_BE.xlsx`** y **`Población_estudiantil_Iciclo2026_Bach_CI.xlsx`** (Formato Excel `.xlsx`, procesados con `openpyxl`): Listas oficiales de población para los énfasis de Bibliotecas Educativas (BE) y Ciencias de la Información (CI) del I Ciclo 2026. Tienen un formato descriptivo inicial y los datos reales inician en la fila 3.

### Documentos de Soporte y Estructura
* **`Bach_BE.pdf`** y **`Bach_CI.pdf`**: Planes de estudio completos para ambos énfasis, de donde se extrae la malla y cursos de transición oficiales.
* **`Estudio del perfil Bach_BE.xlsx`** y **`Estudio del perfil Bach_CS.xlsx`**: Hojas de cálculo con el desglose del análisis del perfil de salida de los estudiantes de ambos énfasis.
