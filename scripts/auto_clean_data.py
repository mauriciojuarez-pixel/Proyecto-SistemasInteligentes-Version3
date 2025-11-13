# scripts/auto_clean_data.py
"""
Módulo: auto_clean_data.py
Descripción:
    Automatiza la limpieza de datasets (CSV, XLSX) ubicados en data/datasets/raw/
    y guarda los resultados procesados en data/datasets/processed/.

Flujo:
    1. Escanea data/datasets/raw/ en busca de nuevos archivos.
    2. Aplica limpieza básica (valores nulos, duplicados, tipos de datos, outliers).
    3. Estandariza nombres de columnas.
    4. Exporta los datos procesados.
"""

import sys
from pathlib import Path
from datetime import datetime
import logging
import pandas as pd

from core.utils.data_cleaner import (
    remove_nulls,
    remove_duplicates,
    normalize_columns,
    detect_noise,
    save_clean_data
)

# --- Configuración de paths ---
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "datasets" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "datasets" / "processed"
LOG_FILE = BASE_DIR / "data" / "outputs" / "logs" / "auto_clean_data.log"

# --- Logger ---
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def log(message: str, level="info"):
    if level == "info":
        logging.info(message)
        print(message)
    elif level == "warning":
        logging.warning(message)
        print(message)
    elif level == "error":
        logging.error(message)
        print(message)

def ensure_directories():
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    log("[INFO] Directorio de datos procesados verificado/creado.")

def clean_file(file_path: Path):
    """Aplica limpieza completa a un archivo individual (CSV o XLSX)."""
    try:
        log(f"[INFO] Procesando archivo: {file_path.name}")

        # Cargar dataset
        if file_path.suffix.lower() == ".csv":
            df = pd.read_csv(file_path)
        elif file_path.suffix.lower() in [".xlsx", ".xls"]:
            df = pd.read_excel(file_path)
        else:
            log(f"[WARN] Tipo de archivo no soportado: {file_path.suffix}", level="warning")
            return

        # Limpieza de datos
        df = remove_nulls(df, strategy="mean")
        df = remove_duplicates(df)
        df = normalize_columns(df)
        df = detect_noise(df, z_thresh=3)

        # Guardar archivo limpio
        output_file = PROCESSED_DATA_DIR / file_path.name
        save_clean_data(df, output_file)
        log(f"[INFO] Archivo limpio guardado en: {output_file}")
    except Exception as e:
        log(f"[ERROR] Error procesando {file_path.name}: {e}", level="error")

def clean_all_files():
    ensure_directories()
    log("=== Iniciando limpieza automática de datasets ===")

    files = list(RAW_DATA_DIR.glob("*.*"))
    if not files:
        log("[WARN] No se encontraron archivos en raw/", level="warning")
        return

    for file_path in files:
        clean_file(file_path)

    log("=== Limpieza automática completada ===")

# --- Ejecución ---
if __name__ == "__main__":
    clean_all_files()
