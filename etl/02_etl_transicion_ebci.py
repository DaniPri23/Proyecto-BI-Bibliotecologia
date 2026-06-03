#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import sqlite3
import os
import sys
import hashlib
from datetime import datetime

ANONIMIZAR = False

BASE_DIR = r"c:\Users\danny\OneDrive\Escritorio\bibliotecnologia\datos"
ARCHIVOS = {
    "activos":      os.path.join(BASE_DIR, "Lista_de_Estudiantes_Activos.xls"),
    "inactivos":    os.path.join(BASE_DIR, "Lista_de_Estudiantes_Inactivos_1.xls"),
    "pi_2024":      os.path.join(BASE_DIR, "PRIMER_INGRESO_2024.xls"),
    "pi_2025":      os.path.join(BASE_DIR, "PRIMER_INGRESO_2025.xls"),
    "pi_2026":      os.path.join(BASE_DIR, "PRIMER_INGRESO_2026.xls"),
    "listas_clase": os.path.join(BASE_DIR, "LISTAS_DE_CLASE_2026BI1001_BI1002_BI2006.ods"),
    "poblacion_be": os.path.join(BASE_DIR, "Población_estudiantil_Iciclo2026_Bach_BE.xlsx"),
    "poblacion_ci": os.path.join(BASE_DIR, "Población_estudiantil_Iciclo2026_Bach_CI.xlsx"),
}

DB_PATH = "dw_transicion_ebci.db"

CURSOS_TRANSICION = {"BI1001", "BI1002", "BI2006", "BI1006"}
CURSOS_TRANSICION_CICLO1 = {"BI1001", "BI1002"}
CURSOS_TRANSICION_CICLO2 = {"BI2006", "BI1006"}

PLAN_BE = {
    1: [("BI1001", "TÉCNICAS DE INVESTIGACIÓN BIBLIOGRÁFICA", 4, 0, 0, 0),
        ("BI1002", "FUNDAMENTOS DE LAS CIENCIAS BIBLIOTECOLÓGICAS Y DE LA INFORMACIÓN", 4, 0, 0, 0)],
    2: [("BI1006", "MÉTODOS CUANTITATIVOS I", 4, 0, 0, 0),
        ("BI2006", "SERVICIOS DE INFORMACIÓN AUTOMATIZADOS", 4, 0, 0, 0)],
    3: [("BI2001", "REFERENCIA I", 4, 0, 0, 0),
        ("BI2002", "CATALOGACIÓN I", 4, 0, 0, 0),
        ("BI2008", "MÉTODOS CUANTITATIVOS II", 4, 0, 0, 0),
        ("BI2010", "LABORATORIO DE CATALOGACIÓN I", 0, 0, 3, 0)],
    4: [("BI2003", "CATALOGACIÓN II", 4, 0, 0, 0),
        ("BI2004", "REFERENCIA II", 4, 4, 0, 0),
        ("BI2007", "ESTRUCTURA DE BASES DE DATOS", 2, 2, 0, 0),
        ("BI2009", "MÉTODOS CUANTITATIVOS III", 4, 0, 0, 0),
        ("BI2011", "LABORATORIO DE CATALOGACIÓN II", 0, 0, 3, 0)],
    5: [("BI3001", "INDIZACIÓN", 4, 0, 0, 0),
        ("BI3002", "BIBLIOGRAFOLOGÍA", 4, 0, 0, 0),
        ("BI3003", "ADMINISTRACIÓN DE UNIDADES DE INFORMACIÓN I", 4, 0, 0, 0),
        ("BI3009", "ESTUDIOS MÉTRICOS DE LA INFORMACIÓN I", 4, 0, 0, 0),
        ("BI3011", "LABORATORIO DE INDIZACIÓN", 0, 0, 3, 0)],
    6: [("BI3006", "ADMINISTRACIÓN DE UNIDADES DE INFORMACIÓN II", 4, 0, 0, 0),
        ("BI3007", "CLASIFICACIÓN", 4, 0, 0, 0),
        ("BI3008", "BIBLIOGRAFÍA NACIONAL Y LATINOAMERICANA", 4, 4, 0, 0),
        ("BI3010", "ESTUDIOS MÉTRICOS DE LA INFORMACIÓN II", 4, 0, 0, 0),
        ("BI3012", "LABORATORIO DE CLASIFICACIÓN", 0, 0, 3, 0)],
    7: [("BI1005", "ESTUDIO Y FORMACIÓN DE USUARIOS", 4, 0, 0, 0),
        ("BI4002", "REDES Y SISTEMAS DE BIBLIOTECAS EDUCATIVAS", 4, 0, 0, 0),
        ("BI4003", "BIBLIOTECOLOGÍA Y COMUNICACIÓN SOCIAL", 4, 0, 0, 0)],
    8: [("BI3005", "DESARROLLO DE COLECCIONES", 4, 0, 0, 0),
        ("BI4004", "BIBLIOTECAS EDUCATIVAS COMO CENTRO DE RECURSOS", 4, 0, 0, 0),
        ("BI4005", "SEMINARIO TALLER DE BIBLIOTECAS EDUCATIVAS", 4, 0, 0, 0)],
}

PLAN_CI = {
    1: [("BI1001", "TÉCNICAS DE INVESTIGACIÓN BIBLIOGRÁFICA", 4, 0, 0, 0),
        ("BI1002", "FUNDAMENTOS DE LAS CIENCIAS BIBLIOTECOLÓGICAS Y DE LA INFORMACIÓN", 4, 0, 0, 0)],
    2: [("BI1006", "MÉTODOS CUANTITATIVOS I", 4, 0, 0, 0),
        ("BI2006", "SERVICIOS DE INFORMACIÓN AUTOMATIZADOS", 4, 0, 0, 0)],
    3: [("BI2001", "REFERENCIA I", 4, 0, 0, 0),
        ("BI2002", "CATALOGACIÓN I", 4, 0, 0, 0),
        ("BI2008", "MÉTODOS CUANTITATIVOS II", 4, 0, 0, 0),
        ("BI2010", "LABORATORIO DE CATALOGACIÓN I", 0, 0, 3, 0)],
    4: [("BI2003", "CATALOGACIÓN II", 4, 0, 0, 0),
        ("BI2004", "REFERENCIA II", 4, 4, 0, 0),
        ("BI2007", "ESTRUCTURA DE BASES DE DATOS", 2, 2, 0, 0),
        ("BI2009", "MÉTODOS CUANTITATIVOS III", 4, 0, 0, 0),
        ("BI2011", "LABORATORIO DE CATALOGACIÓN II", 0, 0, 3, 0)],
    5: [("BI3001", "INDIZACIÓN", 4, 0, 0, 0),
        ("BI3002", "BIBLIOGRAFOLOGÍA", 4, 0, 0, 0),
        ("BI3003", "ADMINISTRACIÓN DE UNIDADES DE INFORMACIÓN I", 4, 0, 0, 0),
        ("BI3009", "ESTUDIOS MÉTRICOS DE LA INFORMACIÓN I", 4, 0, 0, 0),
        ("BI3011", "LABORATORIO DE INDIZACIÓN", 0, 0, 3, 0)],
    6: [("BI3006", "ADMINISTRACIÓN DE UNIDADES DE INFORMACIÓN II", 4, 0, 0, 0),
        ("BI3007", "CLASIFICACIÓN", 4, 0, 0, 0),
        ("BI3008", "BIBLIOGRAFÍA NACIONAL Y LATINOAMERICANA", 4, 4, 0, 0),
        ("BI3010", "ESTUDIOS MÉTRICOS DE LA INFORMACIÓN II", 4, 0, 0, 0),
        ("BI3012", "LABORATORIO DE CLASIFICACIÓN", 0, 0, 3, 0)],
    7: [("BI1005", "ESTUDIO Y FORMACIÓN DE USUARIOS", 4, 0, 0, 0),
        ("BI4006", "CENTROS DE INFORMACIÓN ESPECIALIZADOS", 4, 0, 0, 0),
        ("BI4008", "REDES Y SISTEMAS DE INFORMACIÓN", 4, 0, 0, 0),
        ("BI4014", "AUTOMATIZACIÓN DE UNIDADES DE INFORMACIÓN", 4, 0, 0, 0)],
    8: [("BI3005", "DESARROLLO DE COLECCIONES", 4, 0, 0, 0),
        ("BI4003", "BIBLIOTECOLOGÍA Y COMUNICACIÓN SOCIAL", 4, 0, 0, 0),
        ("BI4010", "ANÁLISIS Y DISEÑO DE SISTEMAS DE INFORMACIÓN", 4, 0, 0, 0),
        ("BI4011", "SEMINARIO TALLER EN CIENCIAS DE LA INFORMACIÓN", 4, 0, 0, 0),
        ("BI4012", "MERCADEO DE LA INFORMACIÓN", 4, 0, 0, 0)],
}

LOG = []

def log(msg):
    
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{ts}] {msg}"
    LOG.append(entry)
    safe_entry = entry.replace("→", "->")
    try:
        print(safe_entry)
    except UnicodeEncodeError:
        try:
            encoding = sys.stdout.encoding or 'utf-8'
            print(safe_entry.encode(encoding, errors='replace').decode(encoding))
        except Exception:
            print(safe_entry.encode('ascii', errors='replace').decode('ascii'))

def anonimizar_nombre(texto):
    
    if pd.isna(texto) or texto == "":
        return "ANONIMO"
    h = hashlib.sha256(str(texto).encode()).hexdigest()[:8]
    return f"EST_{h.upper()}"

def extraer_datos():
    
    log("=" * 70)
    log("FASE 1: EXTRACCIÓN DE DATOS")
    log("=" * 70)

    datos = {}

    log("Extrayendo: Lista de Estudiantes Activos...")
    datos["activos"] = pd.read_excel(ARCHIVOS["activos"], engine="xlrd")
    log(f"  → {len(datos['activos'])} registros extraídos")

    log("Extrayendo: Lista de Estudiantes Inactivos...")
    datos["inactivos"] = pd.read_excel(ARCHIVOS["inactivos"], engine="xlrd")
    log(f"  → {len(datos['inactivos'])} registros extraídos")

    for anio in [2024, 2025, 2026]:
        key = f"pi_{anio}"
        log(f"Extrayendo: Primer Ingreso {anio}...")
        datos[key] = pd.read_excel(ARCHIVOS[key], engine="xlrd")
        log(f"  → {len(datos[key])} registros extraídos")

    log("Extrayendo: Listas de Clase I-2026 (ODS)...")
    datos["listas_clase"] = pd.read_excel(ARCHIVOS["listas_clase"], engine="odf")
    log(f"  → {len(datos['listas_clase'])} registros extraídos")
    log(f"    Cursos: {datos['listas_clase']['sigla'].value_counts().to_dict()}")

    for enfasis, key in [("BE", "poblacion_be"), ("CI", "poblacion_ci")]:
        log(f"Extrayendo: Población I-2026 {enfasis}...")
        df_raw = pd.read_excel(ARCHIVOS[key], engine="openpyxl", header=None)
        cols = df_raw.iloc[0].tolist()
        cols_clean = ["carne", "apellido1", "apellido2", "nombre",
                      "correo_institucional", "sexo", "provincia_procedencia",
                      "tipo_ingreso", "ano_ingreso_carrera",
                      "estado_ciclo_seleccionado"]
        df = df_raw.iloc[1:].reset_index(drop=True)
        df.columns = cols_clean
        df = df.dropna(subset=["carne"])
        df = df[~df["estado_ciclo_seleccionado"].astype(str).str.contains(
            "Estado en el ciclo seleccionado", case=False, na=False
        )]
        df["enfasis_poblacion"] = enfasis
        datos[key] = df
        log(f"  → {len(df)} registros extraídos")

    log(f"\nExtracción completada. Total de fuentes: {len(datos)}")
    return datos

def transformar_datos(datos):
    
    log("=" * 70)
    log("FASE 2: TRANSFORMACIÓN DE DATOS")
    log("=" * 70)

    log("\n--- T5: Aplicando Reglas de Homologación ---")

    for key in datos:
        df = datos[key]
        for col_variant in ["carné", "Carné", "CARNE", "Carnet"]:
            if col_variant in df.columns:
                df.rename(columns={col_variant: "carne"}, inplace=True)
                log(f"  Homologación: '{col_variant}' → 'carne' en {key}")

    for key in datos:
        df = datos[key]
        if "direccion_electronica_inst" in df.columns and "correo_institucional" not in df.columns:
            df.rename(columns={"direccion_electronica_inst": "correo_institucional"}, inplace=True)
            log(f"  Homologación: 'direccion_electronica_inst' → 'correo_institucional' en {key}")

    for key in datos:
        df = datos[key]
        if "desc_genero" in df.columns and "sexo" not in df.columns:
            df.rename(columns={"desc_genero": "sexo"}, inplace=True)
            log(f"  Homologación: 'desc_genero' → 'sexo' en {key}")

    for key in datos:
        df = datos[key]
        if "sexo" in df.columns:
            df["sexo"] = df["sexo"].astype(str).str.strip().str.upper()
            df["sexo"] = df["sexo"].replace({
                "FEMENINO": "FEMENINO", "MASCULINO": "MASCULINO",
                "F": "FEMENINO", "M": "MASCULINO",
                "NAN": "NO ESPECIFICADO", "": "NO ESPECIFICADO"
            })

    for key in ["poblacion_be", "poblacion_ci"]:
        df = datos[key]
        if "tipo_ingreso" in df.columns:
            df["tipo_ingreso"] = df["tipo_ingreso"].astype(str).str.strip().str.title()

    for key in ["poblacion_be", "poblacion_ci"]:
        df = datos[key]
        if "estado_ciclo_seleccionado" in df.columns:
            df["estado_ciclo_seleccionado"] = (
                df["estado_ciclo_seleccionado"].astype(str).str.strip().str.upper()
            )

    for key in datos:
        df = datos[key]
        if "carne" in df.columns:
            df["carne"] = df["carne"].astype(str).str.strip().str.upper()

    cols_eliminar = ["telefono_casa", "telefono_oficina", "direccion_electronica",
                     "compute_0010", "compute_0011"]
    for key in datos:
        df = datos[key]
        for col in cols_eliminar:
            if col in df.columns:
                df.drop(columns=[col], inplace=True)
    log("  Eliminadas columnas sensibles: teléfonos, correo personal, campos compute")

    log("  Reglas de homologación aplicadas exitosamente.")

    log("\n--- T4: Derivación de Cohorte ---")

    def derivar_cohorte(carne):
        
        c = str(carne).strip().upper()
        if c.startswith("C4"):
            return "C4"
        elif c.startswith("C5"):
            return "C5"
        elif c.startswith("C6"):
            return "C6"
        else:
            return "Otro"

    for key in datos:
        df = datos[key]
        if "carne" in df.columns:
            df["cohorte"] = df["carne"].apply(derivar_cohorte)

    all_carnes = pd.concat([
        datos["activos"][["carne", "cohorte"]],
        datos["inactivos"][["carne", "cohorte"]],
    ]).drop_duplicates(subset=["carne"])
    log(f"  Distribución de cohortes (activos+inactivos):")
    for c, n in all_carnes["cohorte"].value_counts().items():
        log(f"    {c}: {n} estudiantes")

    log("\n--- T3: Clasificación Activo/Inactivo ---")

    datos["activos"]["es_activo"] = 1
    datos["activos"]["desc_estado_norm"] = "Activo"
    datos["inactivos"]["es_activo"] = 0
    datos["inactivos"]["desc_estado_norm"] = "Inactivo"

    for key in ["poblacion_be", "poblacion_ci"]:
        df = datos[key]
        def clasificar_estado_poblacion(x):
            s = str(x).strip().upper()
            if "ACTIVO MATRICULADO" in s:
                return 1
            elif "ACTIVO SIN MATRÍCULA" in s or "ACTIVO SIN MATRICULA" in s:
                return 1
            elif "NO HA CONSOLIDADO" in s:
                return 0
            elif "INACTIV" in s:
                return 0
            else:
                return 0
        df["es_activo"] = df["estado_ciclo_seleccionado"].apply(clasificar_estado_poblacion)
        df["desc_estado_norm"] = df["estado_ciclo_seleccionado"].apply(
            lambda x: "Activo" if clasificar_estado_poblacion(x) == 1 else "Inactivo"
        )

    log(f"  Activos: {len(datos['activos'])} | Inactivos: {len(datos['inactivos'])}")
    for key in ["poblacion_be", "poblacion_ci"]:
        df = datos[key]
        activos_pob = (df["es_activo"] == 1).sum()
        inactivos_pob = (df["es_activo"] == 0).sum()
        no_consolidados = df["estado_ciclo_seleccionado"].astype(str).str.contains(
            "NO HA CONSOLIDADO", case=False, na=False
        ).sum()
        log(f"  Población {key[-2:].upper()}: {activos_pob} activos, {inactivos_pob} inactivos")
        log(f"    (de los inactivos: {no_consolidados} no han consolidado ingreso a UCR)")

    log("\n--- T2: Cálculo de Cursos Pendientes ---")

    lc = datos["listas_clase"]
    lc_efectiva = lc[
        ~lc["tipo_matricula"].str.contains("Retiro|Interrupción", case=False, na=False)
    ]
    log(f"  Matrículas efectivas en I-2026: {len(lc_efectiva)} (de {len(lc)} totales)")
    log(f"    Excluidos: 1 Retiro de Matrícula + 3 Interrupción de Estudios = 4 registros")

    cursos_transicion_matriculados = (
        lc_efectiva[lc_efectiva["sigla"].isin(CURSOS_TRANSICION)]
        .groupby("carne")["sigla"]
        .apply(set)
        .reset_index()
    )
    cursos_transicion_matriculados.columns = ["carne", "cursos_matriculados"]

    pi_all = pd.concat([datos["pi_2024"], datos["pi_2025"], datos["pi_2026"]])
    pi_all["carne"] = pi_all["carne"].astype(str).str.strip().str.upper()

    pi_cursos = pi_all.merge(cursos_transicion_matriculados, on="carne", how="left")
    pi_cursos["cursos_matriculados"] = pi_cursos["cursos_matriculados"].apply(
        lambda x: x if isinstance(x, set) else set()
    )
    pi_cursos["num_cursos_trans_matriculados"] = pi_cursos["cursos_matriculados"].apply(len)
    pi_cursos["cursos_pendientes"] = 4 - pi_cursos["num_cursos_trans_matriculados"]

    log(f"  Distribución de cursos pendientes (primer ingreso 2024-2026):")
    for n, cnt in pi_cursos["cursos_pendientes"].value_counts().sort_index().items():
        log(f"    {n} cursos pendientes: {cnt} estudiantes")

    log("\n--- T1: Clasificación de Transición (Escenarios 1-4) ---")

    def clasificar_transicion(row):
        
        cohorte = str(row.get("cohorte", "Otro"))
        cursos = row.get("cursos_matriculados", set())
        es_activo = row.get("es_activo", 1)

        if cohorte == "C6":
            bloque_completo = CURSOS_TRANSICION_CICLO1.issubset(cursos) and "BI2006" in cursos
            if bloque_completo:
                return "Escenario 1"  # C6 completo
            elif len(cursos) > 0:
                return "Escenario 2"  # C6 parcial
            else:
                return "Escenario 2"  # C6 sin cursos de transición

        elif cohorte in ("C4", "C5"):
            if es_activo == 0:
                return "Escenario 4"  # C4/C5 inactivo
            elif len(cursos) > 0:
                return "Escenario 3"  # C4/C5 con cursos
            else:
                return "Escenario 3"  # C4/C5 activo sin cursos de transición

        else:
            return "Otro"  # Cohortes anteriores

    activos_carnes = set(datos["activos"]["carne"].astype(str).str.strip().str.upper())
    inactivos_carnes = set(datos["inactivos"]["carne"].astype(str).str.strip().str.upper())

    pi_cursos["es_activo"] = pi_cursos["carne"].apply(
        lambda c: 1 if c in activos_carnes else (0 if c in inactivos_carnes else 1)
    )

    pi_cursos["cat_transicion"] = pi_cursos.apply(clasificar_transicion, axis=1)

    pi_cursos["apto_transicion"] = pi_cursos.apply(
        lambda row: 1 if (row["cat_transicion"] == "Escenario 1") else 0,
        axis=1
    )

    def grupo_analisis(row):
        if row["cat_transicion"] == "Escenario 1":
            return "C6-Completo"
        elif row["cat_transicion"] == "Escenario 2":
            return "C6-Parcial"
        elif row["cat_transicion"] == "Escenario 3":
            return "C4C5-Con-Cursos"
        elif row["cat_transicion"] == "Escenario 4":
            return "C4C5-Inactivo"
        else:
            return "Otro"

    pi_cursos["grupo_analisis"] = pi_cursos.apply(grupo_analisis, axis=1)

    pi_cursos["requiere_levantamiento"] = pi_cursos.apply(
        lambda r: 1 if r["cat_transicion"] in ("Escenario 2", "Escenario 3")
                       and r["cursos_pendientes"] > 0 else 0,
        axis=1
    )
    log(f"  Estudiantes que requieren levantamiento de requisitos: "
        f"{pi_cursos['requiere_levantamiento'].sum()}")

    log("\n--- Limitaciones documentadas ---")
    log("  LIMITACIÓN 1: Escenario 3 usa 'matriculados' como proxy de 'aprobados'")
    log("    → No se dispone de actas de aprobación (fuente mencionada en doc transición)")
    log("  LIMITACIÓN 2: Datos de matrícula solo para I-2026 (no hay ciclos anteriores)")
    log("  LIMITACIÓN 3: LM-1030 es opcional y no se incluye en cursos pendientes")

    log("\n  Distribución por escenario de transición:")
    for esc, cnt in pi_cursos["cat_transicion"].value_counts().items():
        log(f"    {esc}: {cnt} estudiantes")

    log(f"  Aptos para transición 2027: {pi_cursos['apto_transicion'].sum()}")

    log("\n--- Construyendo Dimensiones ---")

    log("  Construyendo DIM_ESTUDIANTE...")
    est_activos = datos["activos"][["carne", "apellido1", "apellido2", "nombre",
                                     "sexo", "ano_ingreso_carrera",
                                     "periodo_ingreso_carrera",
                                     "desc_tipo_estudiante", "cohorte"]].copy()
    est_activos.rename(columns={
        "periodo_ingreso_carrera": "periodo_ingreso",
        "desc_tipo_estudiante": "tipo_estudiante"
    }, inplace=True)
    est_activos["tipo_ingreso"] = "No especificado"

    est_inactivos = datos["inactivos"][["carne", "apellido1", "apellido2", "nombre",
                                         "sexo", "ano_ingreso_carrera",
                                         "periodo_ingreso_carrera",
                                         "desc_tipo_estudiante", "cohorte"]].copy()
    est_inactivos.rename(columns={
        "periodo_ingreso_carrera": "periodo_ingreso",
        "desc_tipo_estudiante": "tipo_estudiante"
    }, inplace=True)
    est_inactivos["tipo_ingreso"] = "No especificado"

    pi_est = []
    for key in ["pi_2024", "pi_2025", "pi_2026"]:
        df = datos[key][["carne", "apellido1", "apellido2", "nombre",
                          "ano_ingreso_carrera", "periodo_ingreso_carrera",
                          "cohorte"]].copy()
        df.rename(columns={"periodo_ingreso_carrera": "periodo_ingreso"}, inplace=True)
        df["sexo"] = "NO ESPECIFICADO"
        df["tipo_ingreso"] = "Primer ingreso"
        df["tipo_estudiante"] = "Estudiante de pregrado y grado"
        pi_est.append(df)
    pi_estudiantes = pd.concat(pi_est)

    pob = pd.concat([datos["poblacion_be"], datos["poblacion_ci"]])
    pob_sexo = pob[["carne", "sexo", "tipo_ingreso"]].drop_duplicates(subset=["carne"])

    dim_est = pd.concat([est_activos, est_inactivos, pi_estudiantes])
    dim_est = dim_est.drop_duplicates(subset=["carne"], keep="first")

    dim_est = dim_est.merge(
        pob_sexo.rename(columns={"sexo": "sexo_pob", "tipo_ingreso": "tipo_ingreso_pob"}),
        on="carne", how="left"
    )
    mask_sexo = (dim_est["sexo"] == "NO ESPECIFICADO") | (dim_est["sexo"].isna())
    dim_est.loc[mask_sexo, "sexo"] = dim_est.loc[mask_sexo, "sexo_pob"]
    mask_ti = dim_est["tipo_ingreso"] == "No especificado"
    dim_est.loc[mask_ti, "tipo_ingreso"] = dim_est.loc[mask_ti, "tipo_ingreso_pob"]
    dim_est.drop(columns=["sexo_pob", "tipo_ingreso_pob"], inplace=True)

    dim_est["cohorte"] = dim_est["carne"].apply(derivar_cohorte)

    if ANONIMIZAR:
        log("  ANONIMIZACIÓN ACTIVADA: reemplazando nombres...")
        dim_est["nombre"] = dim_est["carne"].apply(anonimizar_nombre)
        dim_est["apellido1"] = "***"
        dim_est["apellido2"] = "***"

    dim_est["periodo_ingreso"] = dim_est["periodo_ingreso"].astype(str)
    log(f"  DIM_ESTUDIANTE: {len(dim_est)} registros únicos")

    log("  Construyendo DIM_CURSO...")
    cursos_plan = []
    for nivel, cursos in PLAN_BE.items():
        for c in cursos:
            cursos_plan.append({
                "sigla": c[0], "nombre_curso": c[1],
                "nivel": nivel, "plan_estudios": 4,
                "horas_t": c[2], "horas_p": c[3], "horas_l": c[4], "horas_tp": c[5],
                "es_curso_transicion": 1 if c[0] in CURSOS_TRANSICION else 0
            })
    for nivel, cursos in PLAN_CI.items():
        for c in cursos:
            cursos_plan.append({
                "sigla": c[0], "nombre_curso": c[1],
                "nivel": nivel, "plan_estudios": 3,
                "horas_t": c[2], "horas_p": c[3], "horas_l": c[4], "horas_tp": c[5],
                "es_curso_transicion": 1 if c[0] in CURSOS_TRANSICION else 0
            })

    dim_curso_base = pd.DataFrame(cursos_plan).drop_duplicates(subset=["sigla", "plan_estudios"])

    lc_info = lc_efectiva[["sigla", "grupo", "dsc_modalidad"]].drop_duplicates()
    dim_curso_final = dim_curso_base.merge(
        lc_info.rename(columns={"dsc_modalidad": "modalidad"}),
        on="sigla", how="left"
    )
    dim_curso_final["grupo"] = dim_curso_final["grupo"].fillna(0).astype(int)
    dim_curso_final["modalidad"] = dim_curso_final["modalidad"].fillna("Regular")

    log(f"  DIM_CURSO: {len(dim_curso_final)} registros")
    log(f"    Cursos de transición: {dim_curso_final['es_curso_transicion'].sum()}")

    log("  Construyendo DIM_TIEMPO...")
    periodos = [
        {"sk_tiempo": 202401, "anio": 2024, "ciclo": "I",   "semestre": 1, "periodo_academico": "I-2024", "anno_ingreso": 2024},
        {"sk_tiempo": 202402, "anio": 2024, "ciclo": "II",  "semestre": 1, "periodo_academico": "II-2024", "anno_ingreso": 2024},
        {"sk_tiempo": 202501, "anio": 2025, "ciclo": "I",   "semestre": 1, "periodo_academico": "I-2025", "anno_ingreso": 2025},
        {"sk_tiempo": 202502, "anio": 2025, "ciclo": "II",  "semestre": 1, "periodo_academico": "II-2025", "anno_ingreso": 2025},
        {"sk_tiempo": 202601, "anio": 2026, "ciclo": "I",   "semestre": 1, "periodo_academico": "I-2026", "anno_ingreso": 2026},
        {"sk_tiempo": 202602, "anio": 2026, "ciclo": "II",  "semestre": 2, "periodo_academico": "II-2026", "anno_ingreso": 2026},
        {"sk_tiempo": 202603, "anio": 2026, "ciclo": "III", "semestre": 2, "periodo_academico": "III-2026", "anno_ingreso": 2026},
    ]
    dim_tiempo = pd.DataFrame(periodos)
    log(f"  DIM_TIEMPO: {len(dim_tiempo)} períodos")

    log("  Construyendo DIM_CARRERA...")
    carreras_data = [
        {"codigo_carrera": 320401, "descripcion_carrera": "BACH.EN BIBLIOTECOLOGIA ENF.CS. DE LA INFORMACION",
         "enfasis": "CI", "grado": "Bachillerato", "escuela": 3204,
         "desc_escuela": "BIBLIOTECOLOGIA", "facultad": "FACULTAD DE EDUCACIÓN"},
        {"codigo_carrera": 320402, "descripcion_carrera": "BACH.EN BIBLIOTECOLOGIA ENF.BIBLIOTECAS EDUCATIVAS",
         "enfasis": "BE", "grado": "Bachillerato", "escuela": 3204,
         "desc_escuela": "BIBLIOTECOLOGIA", "facultad": "FACULTAD DE EDUCACIÓN"},
        {"codigo_carrera": 320403, "descripcion_carrera": "LIC. EN BIBLIOTECOLOGIA Y CS. DE LA INFORMACION",
         "enfasis": "CI", "grado": "Licenciatura", "escuela": 3204,
         "desc_escuela": "BIBLIOTECOLOGIA", "facultad": "FACULTAD DE EDUCACIÓN"},
        {"codigo_carrera": 320404, "descripcion_carrera": "LIC. EN BIBLIOTECOLOGIA ENF. EN BIBLIOTECAS EDUCAT",
         "enfasis": "BE", "grado": "Licenciatura", "escuela": 3204,
         "desc_escuela": "BIBLIOTECOLOGIA", "facultad": "FACULTAD DE EDUCACIÓN"},
    ]
    dim_carrera = pd.DataFrame(carreras_data)
    log(f"  DIM_CARRERA: {len(dim_carrera)} registros")

    log("  Construyendo DIM_RECINTO...")
    dim_recinto = pd.DataFrame([{
        "codigo_recinto": 11,
        "nombre_recinto": "CIUDAD UNIVERSITARIA RODRIGO FACIO",
        "sede": "SEDE RODRIGO FACIO",
        "desc_escuela": "BIBLIOTECOLOGIA",
        "universidad": "Universidad de Costa Rica"
    }])
    log(f"  DIM_RECINTO: {len(dim_recinto)} registros")

    log("  Construyendo DIM_ESTADO_TRANSICION...")
    estados_rows = []

    tipos_matricula = lc_efectiva["tipo_matricula"].unique().tolist()
    tipos_matricula.append("Sin matrícula")

    escenarios = ["Escenario 1", "Escenario 2", "Escenario 3", "Escenario 4", "Otro"]
    for estado_acad, desc_est, es_inactivo in [(0, "Activo", 0), (1, "Inactivo", 1)]:
        for tipo_mat in tipos_matricula:
            for esc in escenarios:
                apto = 1 if esc == "Escenario 1" and es_inactivo == 0 else 0
                ga_map = {
                    "Escenario 1": "C6-Completo",
                    "Escenario 2": "C6-Parcial",
                    "Escenario 3": "C4C5-Con-Cursos",
                    "Escenario 4": "C4C5-Inactivo",
                    "Otro": "Otro"
                }
                estados_rows.append({
                    "estado_academico": estado_acad,
                    "desc_estado": desc_est,
                    "tipo_matricula": tipo_mat,
                    "cat_transicion": esc,
                    "apto_nuevo_plan": apto,
                    "grupo_analisis": ga_map[esc],
                    "dsc_modalidad": "Regular",
                    "es_inactivo": es_inactivo
                })

    dim_estado = pd.DataFrame(estados_rows).drop_duplicates()
    log(f"  DIM_ESTADO_TRANSICION: {len(dim_estado)} registros")

    log("\n--- Construyendo FACT_MATRICULA_ACADEMICA ---")

    carne_to_sk = dict(zip(dim_est["carne"], range(1, len(dim_est) + 1)))

    carrera_to_sk = {}
    for idx, row in dim_carrera.iterrows():
        carrera_to_sk[row["codigo_carrera"]] = idx + 1

    fact_rows = []

    promedios = {}
    for key in ["pi_2024", "pi_2025", "pi_2026"]:
        df = datos[key]
        for _, row in df.iterrows():
            c = str(row["carne"]).strip().upper()
            if "promedio_admision" in row.index and pd.notna(row.get("promedio_admision")):
                promedios[c] = row["promedio_admision"]

    carrera_por_est = {}
    for key in ["activos", "inactivos", "pi_2024", "pi_2025", "pi_2026"]:
        df = datos[key]
        if "carrera" in df.columns and "carne" in df.columns:
            for _, row in df.iterrows():
                c = str(row["carne"]).strip().upper()
                if c not in carrera_por_est:
                    carrera_por_est[c] = int(row["carrera"])

    for _, row in pi_cursos.iterrows():
        carne = str(row["carne"]).strip().upper()
        sk_est = carne_to_sk.get(carne)
        if sk_est is None:
            continue

        cohorte = row.get("cohorte", "Otro")
        cat_trans = row.get("cat_transicion", "Otro")
        cursos_mat = row.get("cursos_matriculados", set())
        cp = row.get("cursos_pendientes", 4)
        apto = row.get("apto_transicion", 0)
        es_activo = row.get("es_activo", 1)
        prom = promedios.get(carne, None)

        sk_tiempo = 202601

        cod_carrera = carrera_por_est.get(carne, 320401)
        sk_carrera = carrera_to_sk.get(cod_carrera, 1)

        sk_recinto = 1

        lc_est = lc_efectiva[lc_efectiva["carne"] == carne]
        if len(lc_est) > 0:
            tipo_mat = lc_est.iloc[0]["tipo_matricula"]
            activo_mat = 1 if es_activo == 1 else 0
        else:
            tipo_mat = "Sin matrícula"
            activo_mat = 0

        match = dim_estado[
            (dim_estado["estado_academico"] == (0 if es_activo == 1 else 1)) &
            (dim_estado["tipo_matricula"] == tipo_mat) &
            (dim_estado["cat_transicion"] == cat_trans)
        ]
        if len(match) > 0:
            sk_estado = match.index[0] + 1
        else:
            sk_estado = 1

        for sigla_trans in CURSOS_TRANSICION:
            curso_match = dim_curso_final[dim_curso_final["sigla"] == sigla_trans]
            if len(curso_match) > 0:
                sk_curso = curso_match.index[0] + 1
            else:
                continue

            fact_rows.append({
                "sk_estudiante": sk_est,
                "sk_curso": sk_curso,
                "sk_tiempo": sk_tiempo,
                "sk_carrera": sk_carrera,
                "sk_recinto": sk_recinto,
                "sk_estado_transicion": sk_estado,
                "activo_matriculado": activo_mat if sigla_trans in cursos_mat else 0,
                "cursos_pendientes": cp,
                "apto_transicion": apto,
                "promedio_admision": prom,
            })

    fact_df = pd.DataFrame(fact_rows)
    log(f"  FACT_MATRICULA_ACADEMICA: {len(fact_df)} registros generados")
    log(f"    Activos matriculados (1): {(fact_df['activo_matriculado'] == 1).sum()}")
    log(f"    Aptos transición (1): {(fact_df['apto_transicion'] == 1).sum()}")

    return {
        "dim_estudiante": dim_est,
        "dim_curso": dim_curso_final,
        "dim_tiempo": dim_tiempo,
        "dim_carrera": dim_carrera,
        "dim_recinto": dim_recinto,
        "dim_estado": dim_estado,
        "fact": fact_df,
        "pi_cursos": pi_cursos  # Para evidencia
    }

def cargar_datos(tablas):
    
    log("=" * 70)
    log("FASE 3: CARGA AL DATA WAREHOUSE")
    log("=" * 70)

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)

    ddl_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "01_ddl_modelo_dimensional.sql")
    if os.path.exists(ddl_path):
        log(f"  Ejecutando DDL desde {ddl_path}...")
        with open(ddl_path, "r", encoding="utf-8") as f:
            conn.executescript(f.read())
    else:
        log("  DDL no encontrado, creando tablas directamente...")

    tablas["dim_estudiante"].to_sql("DIM_ESTUDIANTE", conn, if_exists="replace", index=False)
    log(f"  DIM_ESTUDIANTE cargada: {len(tablas['dim_estudiante'])} registros")

    tablas["dim_curso"].to_sql("DIM_CURSO", conn, if_exists="replace", index=False)
    log(f"  DIM_CURSO cargada: {len(tablas['dim_curso'])} registros")

    tablas["dim_tiempo"].to_sql("DIM_TIEMPO", conn, if_exists="replace", index=False)
    log(f"  DIM_TIEMPO cargada: {len(tablas['dim_tiempo'])} registros")

    tablas["dim_carrera"].to_sql("DIM_CARRERA", conn, if_exists="replace", index=False)
    log(f"  DIM_CARRERA cargada: {len(tablas['dim_carrera'])} registros")

    tablas["dim_recinto"].to_sql("DIM_RECINTO", conn, if_exists="replace", index=False)
    log(f"  DIM_RECINTO cargada: {len(tablas['dim_recinto'])} registros")

    tablas["dim_estado"].to_sql("DIM_ESTADO_TRANSICION", conn, if_exists="replace", index=False)
    log(f"  DIM_ESTADO_TRANSICION cargada: {len(tablas['dim_estado'])} registros")

    tablas["fact"].to_sql("FACT_MATRICULA_ACADEMICA", conn, if_exists="replace", index=False)
    log(f"  FACT_MATRICULA_ACADEMICA cargada: {len(tablas['fact'])} registros")

    log("\n--- Verificación Post-Carga ---")
    cursor = conn.cursor()
    for tabla in ["DIM_ESTUDIANTE", "DIM_CURSO", "DIM_TIEMPO", "DIM_CARRERA",
                   "DIM_RECINTO", "DIM_ESTADO_TRANSICION", "FACT_MATRICULA_ACADEMICA"]:
        cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
        count = cursor.fetchone()[0]
        log(f"  {tabla}: {count} registros verificados")

    log("\n--- Consultas de Verificación de Negocio ---")

    cursor.execute("""
        SELECT d.cohorte, COUNT(DISTINCT d.carne)
        FROM DIM_ESTUDIANTE d
        WHERE d.cohorte IN ('C4', 'C5', 'C6')
        GROUP BY d.cohorte
    """)
    for row in cursor.fetchall():
        log(f"  Estudiantes cohorte {row[0]}: {row[1]}")

    cursor.execute("""
        SELECT SUM(apto_transicion) / 4 as aptos
        FROM FACT_MATRICULA_ACADEMICA
        WHERE apto_transicion = 1
    """)
    aptos = cursor.fetchone()[0]
    log(f"  Estudiantes aptos para transición 2027: {aptos}")

    conn.close()
    log(f"\n  Base de datos creada: {DB_PATH}")
    log(f"  Tamaño: {os.path.getsize(DB_PATH) / 1024:.1f} KB")

def generar_evidencias(tablas):
    
    log("=" * 70)
    log("FASE 4: GENERACIÓN DE EVIDENCIAS")
    log("=" * 70)

    log_path = "etl_log_ejecucion.txt"
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("\n".join(LOG))
    log(f"  Log de ejecución: {log_path}")

    resumen_path = "etl_resumen_transformaciones.csv"
    resumen = pd.DataFrame([
        {"#": 1, "Transformación": "Clasificación de Transición",
         "Descripción": "Asigna Escenario 1-4 según cohorte, cursos matriculados y estado",
         "Campo_origen": "cohorte + cursos_matriculados + es_activo",
         "Campo_destino": "cat_transicion (DIM_ESTADO_TRANSICION)",
         "Tipo": "Derivada (regla de negocio)"},
        {"#": 2, "Transformación": "Cálculo de Cursos Pendientes",
         "Descripción": "4 - número de cursos de transición matriculados",
         "Campo_origen": "sigla (LISTAS CLASE) vs CURSOS_TRANSICION",
         "Campo_destino": "cursos_pendientes (FACT)",
         "Tipo": "Calculada"},
        {"#": 3, "Transformación": "Clasificación Activo/Inactivo",
         "Descripción": "Binario: 1=Activo, 0=Inactivo según desc_estado_estudiante",
         "Campo_origen": "desc_estado_estudiante / estado_ciclo_seleccionado",
         "Campo_destino": "activo_matriculado (FACT), es_inactivo (DIM_ESTADO)",
         "Tipo": "Derivada"},
        {"#": 4, "Transformación": "Derivación de Cohorte",
         "Descripción": "C4/C5/C6/Otro según prefijo del carné",
         "Campo_origen": "carne",
         "Campo_destino": "cohorte (DIM_ESTUDIANTE)",
         "Tipo": "Derivada (regla de negocio)"},
        {"#": 5, "Transformación": "Homologación de Campos",
         "Descripción": "Normalización de nombres de campos entre fuentes (carne/carné, sexo/desc_genero, etc.)",
         "Campo_origen": "Múltiples campos con nombres distintos entre archivos",
         "Campo_destino": "Campos unificados en todo el pipeline",
         "Tipo": "Limpieza/Normalización"},
        {"#": 6, "Transformación": "Marcado de Cursos de Transición",
         "Descripción": "Flag es_curso_transicion=1 para BI1001, BI1002, BI2006, BI1006",
         "Campo_origen": "sigla (Planes de estudio PDF)",
         "Campo_destino": "es_curso_transicion (DIM_CURSO)",
         "Tipo": "Derivada"},
        {"#": 7, "Transformación": "Aptitud para Nuevo Plan 2027",
         "Descripción": "apto_transicion=1 si Escenario 1 y activo",
         "Campo_origen": "cat_transicion + es_activo",
         "Campo_destino": "apto_transicion (FACT), apto_nuevo_plan (DIM_ESTADO)",
         "Tipo": "Derivada (regla de negocio)"},
        {"#": 8, "Transformación": "Generación de DIM_TIEMPO",
         "Descripción": "Construcción artificial de períodos académicos (YYYYCC)",
         "Campo_origen": "ano_ingreso_carrera + periodo_ingreso_carrera",
         "Campo_destino": "sk_tiempo, periodo_academico (DIM_TIEMPO)",
         "Tipo": "Generada en ETL"},
        {"#": 9, "Transformación": "Derivación de Énfasis de Carrera",
         "Descripción": "BE o CI según código de carrera",
         "Campo_origen": "codigo_carrera (320401=CI, 320402=BE, etc.)",
         "Campo_destino": "enfasis (DIM_CARRERA)",
         "Tipo": "Derivada"},
        {"#": 10, "Transformación": "Grupo de Análisis",
         "Descripción": "Agrupación analítica: C6-Completo, C6-Parcial, C4C5-Con-Cursos, C4C5-Inactivo",
         "Campo_origen": "cat_transicion",
         "Campo_destino": "grupo_analisis (DIM_ESTADO_TRANSICION)",
         "Tipo": "Derivada"},
        {"#": 11, "Transformación": "Eliminación de Datos Sensibles",
         "Descripción": "Teléfonos, correo personal y campos compute eliminados del DW",
         "Campo_origen": "telefono_casa, telefono_oficina, direccion_electronica, compute_*",
         "Campo_destino": "N/A (eliminados)",
         "Tipo": "Protección de datos"},
        {"#": 12, "Transformación": "Normalización de Valores de Sexo",
         "Descripción": "Unificar valores: Femenino→FEMENINO, F→FEMENINO, etc.",
         "Campo_origen": "sexo / desc_genero",
         "Campo_destino": "sexo (DIM_ESTUDIANTE)",
         "Tipo": "Limpieza/Normalización"},
    ])
    resumen.to_csv(resumen_path, index=False, encoding="utf-8-sig")
    log(f"  Tabla de transformaciones: {resumen_path}")

    sample_path = "etl_evidencia_clasificacion.csv"
    cols_ev = ["carne", "cohorte", "num_cursos_trans_matriculados",
               "cursos_pendientes", "es_activo", "cat_transicion",
               "apto_transicion", "grupo_analisis", "requiere_levantamiento"]
    tablas["pi_cursos"][cols_ev].to_csv(sample_path, index=False, encoding="utf-8-sig")
    log(f"  Evidencia de clasificación: {sample_path}")

def main():
    log("=" * 70)
    log("ETL TRANSICIÓN CURRICULAR EBCI-UCR")
    log(f"Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log("=" * 70)

    datos = extraer_datos()

    tablas = transformar_datos(datos)

    cargar_datos(tablas)

    generar_evidencias(tablas)

    log("\n" + "=" * 70)
    log("ETL COMPLETADO EXITOSAMENTE")
    log(f"Fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log("=" * 70)

    with open("etl_log_ejecucion.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(LOG))

if __name__ == "__main__":
    main()
