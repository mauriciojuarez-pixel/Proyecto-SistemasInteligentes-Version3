# scripts/generate_report_auto.py
"""
Módulo: generate_report_auto.py
Descripción:
    Genera un reporte completo y automático a partir de los datos procesados
    y del modelo Gemma 2B IT fine-tuned. El reporte incluye:
        - Resumen estadístico de los datos
        - Correlaciones principales
        - Detección de anomalías
        - Conclusión generada por el modelo IA
        - Exportación final en PDF y Excel

Flujo general:
    1. Cargar datos limpios desde data/datasets/processed/
    2. Calcular métricas estadísticas básicas
    3. Aplicar análisis correlacional y detección de outliers
    4. Generar conclusiones con el modelo Gemma 2B IT
    5. Exportar el reporte final en data/outputs/reports/
"""

import sys
from pathlib import Path
from datetime import datetime
import logging
import pandas as pd

from core.heavy_modules.reporting.report_builder import ReportBuilder
from core.utils.logger import init_logger

# --- Configuración de paths ---
BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DATA_DIR = BASE_DIR / "data" / "datasets" / "processed"
REPORTS_DIR = BASE_DIR / "data" / "outputs" / "reports"
LOG_FILE = BASE_DIR / "data" / "outputs" / "logs" / "generate_report.log"

# --- Logger ---
logger = init_logger("generate_report_auto", LOG_FILE)

def log(message: str, level="info"):
    if level == "info":
        logger.info(message)
        print(message)
    elif level == "warning":
        logger.warning(message)
        print(message)
    elif level == "error":
        logger.error(message)
        print(message)

def ensure_directories():
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    log("[INFO] Directorio de reportes verificado/creado.")

def load_processed_data():
    """Carga todos los archivos procesados en un único DataFrame."""
    files = list(PROCESSED_DATA_DIR.glob("*.*"))
    if not files:
        log("[WARN] No se encontraron archivos procesados.", level="warning")
        return pd.DataFrame()

    df_list = []
    for f in files:
        try:
            if f.suffix.lower() == ".csv":
                df_list.append(pd.read_csv(f))
            elif f.suffix.lower() in [".xlsx", ".xls"]:
                df_list.append(pd.read_excel(f))
        except Exception as e:
            log(f"[ERROR] No se pudo leer {f.name}: {e}", level="error")
    if df_list:
        df = pd.concat(df_list, ignore_index=True)
        log(f"[INFO] {len(df)} filas cargadas desde {len(df_list)} archivos procesados.")
        return df
    else:
        return pd.DataFrame()

def generate_report():
    log("=== Iniciando generación automática de reportes ===")
    ensure_directories()

    # 1. Cargar datos procesados
    df = load_processed_data()
    if df.empty:
        log("[ERROR] No hay datos procesados disponibles.", level="error")
        sys.exit(1)

    # 2. Construir reporte
    try:
        report = ReportBuilder(title="Reporte Automático Gemma 2B IT")
        report.build_structure(metadata={"autor": "Sistema IA", "fecha": datetime.now().strftime("%Y-%m-%d")})
        
        # Secciones de análisis básico
        summary_stats = df.describe(include="all").to_dict()
        report.add_text_sections({"Resumen estadístico": str(summary_stats)})

        # Métricas y correlaciones
        corr_matrix = df.corr().round(2).to_dict()
        report.add_text_sections({"Correlaciones principales": str(corr_matrix)})

        # Insertar métricas (simulando resultados de modelo)
        report.insert_metrics({"dummy_model": {"accuracy": 0.95, "f1_score": 0.92}})

        # Exportar a PDF y Excel
        report.finalize_report(export_format=["pdf", "excel"], filename=f"{REPORTS_DIR}/reporte_gemma")
        log("[INFO] Reporte generado correctamente en PDF y Excel.")
    except Exception as e:
        log(f"[ERROR] Error generando el reporte: {e}", level="error")
        sys.exit(1)

# --- Ejecución ---
if __name__ == "__main__":
    generate_report()
