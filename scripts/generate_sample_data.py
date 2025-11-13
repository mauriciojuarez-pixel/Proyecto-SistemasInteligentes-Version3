# scripts/generate_sample_data.py
"""
Módulo: generate_sample_data.py
Descripción:
    Genera datasets sintéticos para pruebas del sistema.
    Soporta CSV y Excel, con posibilidad de añadir ruido controlado.
    Archivos generados en data/datasets/samples/.
"""

from pathlib import Path
from datetime import datetime
import random
import logging
import pandas as pd

# --- Configuración de paths ---
BASE_DIR = Path(__file__).resolve().parent.parent
SAMPLES_DIR = BASE_DIR / "data" / "datasets" / "samples"
LOG_FILE = BASE_DIR / "data" / "outputs" / "logs" / "generate_sample_data.log"

# --- Logger ---
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("generate_sample_data")

def log(message: str, level="info"):
    """Logger unificado con consola."""
    if level == "info":
        logger.info(message)
    elif level == "warning":
        logger.warning(message)
    elif level == "error":
        logger.error(message)
    print(message)

# --- Funciones principales ---
def generate_sample_rows(num_rows=100):
    """Genera una lista de diccionarios con datos sintéticos."""
    rows = []
    for i in range(1, num_rows + 1):
        rows.append({
            "id": i,
            "feature1": round(random.uniform(0, 100), 2),
            "feature2": round(random.uniform(0, 50), 2),
            "feature3": round(random.uniform(10, 500), 2),
            "label": random.choice([0, 1])
        })
    return rows

def add_noise(df: pd.DataFrame, noise_level=0.05):
    """Introduce ruido aleatorio a valores numéricos del DataFrame."""
    numeric_cols = df.select_dtypes(include="number").columns
    for col in numeric_cols:
        df[col] = df[col].apply(lambda x: x * (1 + random.uniform(-noise_level, noise_level)))
    return df

def save_csv(df: pd.DataFrame, filename="sample_data.csv"):
    file_path = SAMPLES_DIR / filename
    df.to_csv(file_path, index=False)
    log(f"[INFO] CSV generado: {file_path}")
    return file_path

def save_excel(df: pd.DataFrame, filename="sample_data.xlsx"):
    file_path = SAMPLES_DIR / filename
    df.to_excel(file_path, index=False)
    log(f"[INFO] Excel generado: {file_path}")
    return file_path

def generate_sample_data(num_rows=100, add_noise_flag=False):
    """Genera dataset sintético en CSV y Excel."""
    SAMPLES_DIR.mkdir(parents=True, exist_ok=True)
    log(f"[INFO] Directorio de samples verificado: {SAMPLES_DIR}")

    rows = generate_sample_rows(num_rows)
    df = pd.DataFrame(rows)

    if add_noise_flag:
        df = add_noise(df)
        log(f"[INFO] Ruido agregado a los datos (±{5}%)")

    csv_path = save_csv(df)
    excel_path = save_excel(df)
    return csv_path, excel_path

# --- Ejecución directa ---
if __name__ == "__main__":
    generate_sample_data(num_rows=100, add_noise_flag=True)
