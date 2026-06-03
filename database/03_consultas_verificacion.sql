
SELECT 'DIM_ESTUDIANTE' AS tabla, COUNT(*) AS registros FROM DIM_ESTUDIANTE
UNION ALL
SELECT 'DIM_CURSO', COUNT(*) FROM DIM_CURSO
UNION ALL
SELECT 'DIM_TIEMPO', COUNT(*) FROM DIM_TIEMPO
UNION ALL
SELECT 'DIM_CARRERA', COUNT(*) FROM DIM_CARRERA
UNION ALL
SELECT 'DIM_RECINTO', COUNT(*) FROM DIM_RECINTO
UNION ALL
SELECT 'DIM_ESTADO_TRANSICION', COUNT(*) FROM DIM_ESTADO_TRANSICION
UNION ALL
SELECT 'FACT_MATRICULA_ACADEMICA', COUNT(*) FROM FACT_MATRICULA_ACADEMICA;

SELECT cohorte, COUNT(*) AS total_estudiantes
FROM DIM_ESTUDIANTE
WHERE cohorte IN ('C4', 'C5', 'C6')
GROUP BY cohorte
ORDER BY cohorte;

SELECT sigla, nombre_curso, nivel, plan_estudios, es_curso_transicion
FROM DIM_CURSO
WHERE es_curso_transicion = 1
ORDER BY plan_estudios, nivel, sigla;

SELECT e.cat_transicion, e.grupo_analisis, COUNT(DISTINCT f.sk_estudiante) AS estudiantes
FROM FACT_MATRICULA_ACADEMICA f
JOIN DIM_ESTADO_TRANSICION e ON f.sk_estado_transicion = e.rowid
GROUP BY e.cat_transicion, e.grupo_analisis
ORDER BY e.cat_transicion;

SELECT d.cohorte, COUNT(DISTINCT f.sk_estudiante) AS aptos
FROM FACT_MATRICULA_ACADEMICA f
JOIN DIM_ESTUDIANTE d ON f.sk_estudiante = d.rowid
WHERE f.apto_transicion = 1
GROUP BY d.cohorte;

SELECT d.cohorte,
       f.cursos_pendientes,
       COUNT(DISTINCT f.sk_estudiante) AS estudiantes
FROM FACT_MATRICULA_ACADEMICA f
JOIN DIM_ESTUDIANTE d ON f.sk_estudiante = d.rowid
WHERE d.cohorte IN ('C4', 'C5', 'C6')
GROUP BY d.cohorte, f.cursos_pendientes
ORDER BY d.cohorte, f.cursos_pendientes;

SELECT d.cohorte,
       CASE WHEN f.activo_matriculado = 1 THEN 'Activo Matriculado'
            ELSE 'No matriculado/Inactivo' END AS estado,
       COUNT(DISTINCT f.sk_estudiante) AS total
FROM FACT_MATRICULA_ACADEMICA f
JOIN DIM_ESTUDIANTE d ON f.sk_estudiante = d.rowid
WHERE d.cohorte IN ('C4', 'C5', 'C6')
GROUP BY d.cohorte, estado
ORDER BY d.cohorte;

SELECT d.cohorte,
       ROUND(AVG(f.promedio_admision), 2) AS promedio_admision_avg,
       ROUND(MIN(f.promedio_admision), 2) AS promedio_min,
       ROUND(MAX(f.promedio_admision), 2) AS promedio_max,
       COUNT(DISTINCT d.carne) AS estudiantes
FROM FACT_MATRICULA_ACADEMICA f
JOIN DIM_ESTUDIANTE d ON f.sk_estudiante = d.rowid
WHERE f.promedio_admision IS NOT NULL
  AND d.cohorte IN ('C4', 'C5', 'C6')
GROUP BY d.cohorte;

SELECT c.enfasis, c.grado, d.cohorte,
       COUNT(DISTINCT f.sk_estudiante) AS total
FROM FACT_MATRICULA_ACADEMICA f
JOIN DIM_ESTUDIANTE d ON f.sk_estudiante = d.rowid
JOIN DIM_CARRERA c ON f.sk_carrera = c.rowid
WHERE d.cohorte IN ('C4', 'C5', 'C6')
GROUP BY c.enfasis, c.grado, d.cohorte
ORDER BY c.enfasis, c.grado, d.cohorte;

SELECT * FROM DIM_TIEMPO ORDER BY sk_tiempo;

