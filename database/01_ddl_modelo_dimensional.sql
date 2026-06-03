
DROP TABLE IF EXISTS FACT_MATRICULA_ACADEMICA;
DROP TABLE IF EXISTS DIM_ESTUDIANTE;
DROP TABLE IF EXISTS DIM_CURSO;
DROP TABLE IF EXISTS DIM_TIEMPO;
DROP TABLE IF EXISTS DIM_CARRERA;
DROP TABLE IF EXISTS DIM_RECINTO;
DROP TABLE IF EXISTS DIM_ESTADO_TRANSICION;

CREATE TABLE DIM_ESTUDIANTE (
    sk_estudiante       INTEGER PRIMARY KEY AUTOINCREMENT,
    carne               VARCHAR(10)  NOT NULL UNIQUE,
    apellido1           VARCHAR(50),
    apellido2           VARCHAR(50),
    nombre              VARCHAR(100),
    sexo                VARCHAR(20),
    tipo_ingreso        VARCHAR(50),
    ano_ingreso_carrera INTEGER,
    periodo_ingreso     VARCHAR(5),
    tipo_estudiante     VARCHAR(60),
    cohorte             VARCHAR(5)
);

CREATE TABLE DIM_CURSO (
    sk_curso            INTEGER PRIMARY KEY AUTOINCREMENT,
    sigla               VARCHAR(10)  NOT NULL,
    nombre_curso        VARCHAR(150),
    nivel               INTEGER,
    plan_estudios       INTEGER,
    es_curso_transicion INTEGER DEFAULT 0,
    grupo               INTEGER,
    modalidad           VARCHAR(30)
);

CREATE TABLE DIM_TIEMPO (
    sk_tiempo           INTEGER PRIMARY KEY,
    anio                INTEGER NOT NULL,
    ciclo               VARCHAR(5),
    semestre            INTEGER,
    periodo_academico   VARCHAR(10),
    anno_ingreso        INTEGER
);

CREATE TABLE DIM_CARRERA (
    sk_carrera          INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_carrera      INTEGER NOT NULL,
    descripcion_carrera VARCHAR(100),
    enfasis             VARCHAR(10),
    grado               VARCHAR(30),
    escuela             INTEGER,
    desc_escuela        VARCHAR(80),
    facultad            VARCHAR(80) DEFAULT 'FACULTAD DE EDUCACIÓN'
);

CREATE TABLE DIM_RECINTO (
    sk_recinto          INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_recinto      INTEGER NOT NULL,
    nombre_recinto      VARCHAR(100),
    sede                VARCHAR(80),
    desc_escuela        VARCHAR(80),
    universidad         VARCHAR(50) DEFAULT 'Universidad de Costa Rica'
);

CREATE TABLE DIM_ESTADO_TRANSICION (
    sk_estado_transicion INTEGER PRIMARY KEY AUTOINCREMENT,
    estado_academico     INTEGER,
    desc_estado          VARCHAR(30),
    tipo_matricula       VARCHAR(80),
    cat_transicion       VARCHAR(30),
    apto_nuevo_plan      INTEGER DEFAULT 0,
    grupo_analisis       VARCHAR(50),
    dsc_modalidad        VARCHAR(30),
    es_inactivo          INTEGER DEFAULT 0
);

CREATE TABLE FACT_MATRICULA_ACADEMICA (
    sk_estudiante        INTEGER NOT NULL,
    sk_curso             INTEGER NOT NULL,
    sk_tiempo            INTEGER NOT NULL,
    sk_carrera           INTEGER NOT NULL,
    sk_recinto           INTEGER NOT NULL,
    sk_estado_transicion INTEGER NOT NULL,
    activo_matriculado   INTEGER DEFAULT 0,
    cursos_pendientes    INTEGER DEFAULT 0,
    apto_transicion      INTEGER DEFAULT 0,
    promedio_admision    REAL,
    FOREIGN KEY (sk_estudiante)        REFERENCES DIM_ESTUDIANTE(sk_estudiante),
    FOREIGN KEY (sk_curso)             REFERENCES DIM_CURSO(sk_curso),
    FOREIGN KEY (sk_tiempo)            REFERENCES DIM_TIEMPO(sk_tiempo),
    FOREIGN KEY (sk_carrera)           REFERENCES DIM_CARRERA(sk_carrera),
    FOREIGN KEY (sk_recinto)           REFERENCES DIM_RECINTO(sk_recinto),
    FOREIGN KEY (sk_estado_transicion) REFERENCES DIM_ESTADO_TRANSICION(sk_estado_transicion)
);

CREATE INDEX idx_fact_estudiante ON FACT_MATRICULA_ACADEMICA(sk_estudiante);
CREATE INDEX idx_fact_curso      ON FACT_MATRICULA_ACADEMICA(sk_curso);
CREATE INDEX idx_fact_tiempo     ON FACT_MATRICULA_ACADEMICA(sk_tiempo);
CREATE INDEX idx_fact_carrera    ON FACT_MATRICULA_ACADEMICA(sk_carrera);
CREATE INDEX idx_fact_estado     ON FACT_MATRICULA_ACADEMICA(sk_estado_transicion);

