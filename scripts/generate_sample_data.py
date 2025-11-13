# scripts/generate_sample_data.py
"""
Módulo: generate_sample_data.py
Descripción:
    Genera datasets de ejemplo (CSV y Excel) para probar el sistema de análisis,
    limpieza, entrenamiento y reporte.

    Los archivos se guardan automáticamente en:
    - data/datasets/raw/
    - data/datasets/processed/ (si se activa la opción de limpieza automática)

Flujo:
    1. Genera datos simulados con pandas y faker.
    2. Crea variaciones aleatorias con ruido controlado.
    3. Exporta los resultados a formato CSV y XLSX.
"""

# scripts/generate_sample_data.py

import csv
from pathlib import Path
from datetime import datetime
import random

BASE_DIR = Path(__file__).resolve().parent.parent
SAMPLES_DIR = BASE_DIR / "data" / "datasets" / "samples"
LOG_FILE = BASE_DIR / "data" / "outputs" / "logs" / "generate_sample_data.log"

def log(message: str):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(message)

def generate_sample_data(filename="sample_data.csv", num_rows=100):
    SAMPLES_DIR.mkdir(parents=True, exist_ok=True)
    file_path = SAMPLES_DIR / filename

    if file_path.exists():
        log(f"[WARN] El archivo {filename} ya existe. Será sobrescrito.")
    
    fields = ["id", "feature1", "feature2", "feature3", "label"]
    
    with open(file_path, mode="w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        for i in range(1, num_rows + 1):
            writer.writerow({
                "id": i,
                "feature1": round(random.uniform(0, 100), 2),
                "feature2": round(random.uniform(0, 50), 2),
                "feature3": round(random.uniform(10, 500), 2),
                "label": random.choice([0, 1])
            })
    
    log(f"[INFO] Archivo de muestra generado: {file_path} con {num_rows} registros.")

if __name__ == "__main__":
    generate_sample_data()
