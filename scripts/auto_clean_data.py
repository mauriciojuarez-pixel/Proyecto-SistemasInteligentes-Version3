# scripts/auto_clean_data.py
"""
Módulo: auto_clean_data.py
Descripción:
    Limpieza automática de datasets ubicados en data/datasets/raw/
    y guardado en data/datasets/processed/ usando DataManager del core.

Funciones principales:
    - scan_raw_folder(): busca archivos nuevos en raw/
    - clean_dataset(file_path): limpia y guarda cada dataset
    - log_cleaning_results(): mantiene registro de la limpieza
"""

from pathlib import Path
import logging
import sys
import pandas as pd

from core.controller.data_manager import DataManager

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

# --- Instanciar DataManager ---
data_manager = DataManager()

# -------------------------------------------------------------------------
# Funciones principales
# -------------------------------------------------------------------------
def scan_raw_folder():
    """Busca archivos CSV y XLSX en raw/"""
    files = list(RAW_DATA_DIR.glob("*.csv")) + list(RAW_DATA_DIR.glob("*.xlsx"))
    return files

def clean_dataset(file_path: Path):
    """Limpia y guarda un dataset usando DataManager"""
    try:
        log(f"[INFO] Procesando archivo: {file_path.name}")

        # Cargar dataset
        df = pd.read_csv(file_path) if file_path.suffix.lower() == ".csv" else pd.read_excel(file_path)

        # Limpieza usando core
        df_clean = data_manager.clean_data(df)

        # Guardar dataset limpio
        output_file = PROCESSED_DATA_DIR / file_path.name
        data_manager.save_processed(df_clean, file_path.name)
        log(f"[INFO] Archivo limpio guardado en: {output_file}")

    except Exception as e:
        log(f"[ERROR] Error procesando {file_path.name}: {e}", level="error")

def clean_all_files():
    """Itera todos los archivos nuevos y aplica limpieza automática"""
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    log("=== Iniciando limpieza automática de datasets ===")

    files = scan_raw_folder()
    if not files:
        log("[WARN] No se encontraron archivos en raw/", level="warning")
        return

    for file_path in files:
        clean_dataset(file_path)

    log("=== Limpieza automática completada ===")

# -------------------------------------------------------------------------
# Ejecución directa
# -------------------------------------------------------------------------
if __name__ == "__main__":
    clean_all_files()
