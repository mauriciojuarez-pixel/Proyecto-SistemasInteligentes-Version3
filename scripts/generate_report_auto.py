# scripts/generate_report_auto.py
"""
Módulo: generate_report_auto.py
Descripción:
    Genera automáticamente un reporte completo en PDF y Excel
    a partir de los datasets procesados y el modelo Gemma 2B IT.
    La lógica de análisis y generación está delegada al core.
"""

import sys
from pathlib import Path
from datetime import datetime
import logging
import pandas as pd

from core.controller.data_manager import DataManager
from core.controller.report_manager import ReportManager

# --- Configuración de paths ---
BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DATA_DIR = BASE_DIR / "data" / "datasets" / "processed"
REPORTS_DIR = BASE_DIR / "data" / "outputs" / "reports"
LOG_FILE = BASE_DIR / "data" / "outputs" / "logs" / "generate_report.log"

# --- Logger ---
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger()

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

def load_all_processed_data() -> pd.DataFrame:
    """Carga todos los archivos procesados en un único DataFrame usando DataManager."""
    data_manager = DataManager()
    files = list(PROCESSED_DATA_DIR.glob("*.*"))
    if not files:
        log("[WARN] No se encontraron archivos procesados.", level="warning")
        return pd.DataFrame()

    df_list = []
    for f in files:
        try:
            df_list.append(data_manager.load_data(str(f)))
        except Exception as e:
            log(f"[ERROR] No se pudo leer {f.name}: {e}", level="error")

    if df_list:
        df = pd.concat(df_list, ignore_index=True)
        log(f"[INFO] {len(df)} filas cargadas desde {len(df_list)} archivos procesados.")
        return df
    else:
        return pd.DataFrame()

def generate_report_auto():
    """Genera el reporte final delegando la lógica al core."""
    log("=== Iniciando generación automática de reportes ===")
    ensure_directories()

    # 1. Cargar datos procesados
    df = load_all_processed_data()
    if df.empty:
        log("[ERROR] No hay datos procesados disponibles.", level="error")
        sys.exit(1)

    try:
        # 2. Crear ReportManager y generar reporte
        report_manager = ReportManager()

        # Resumen del dataset
        summary = df.describe(include="all").to_dict()
        report_manager.append_metadata({
            "autor": "Sistema IA",
            "fecha": datetime.now().strftime("%Y-%m-%d"),
            "filas": len(df),
            "columnas": list(df.columns),
            "resumen": summary
        })

        # Insights y métricas ficticias (se pueden reemplazar con análisis real del modelo)
        # Generar texto interpretativo real usando el modelo
        interpretative_text = report_manager.generate_interpretative_text(df)  # Nueva función
        insights = {"Conclusión automática": interpretative_text}
        report_manager.generate_report(df)

        
        # Exportar reporte final
        pdf_file = report_manager.export_to_pdf()
        excel_file = report_manager.export_to_excel()
        log(f"[INFO] Reporte generado correctamente: PDF -> {pdf_file}, Excel -> {excel_file}")

    except Exception as e:
        log(f"[ERROR] Error generando el reporte: {e}", level="error")
        sys.exit(1)

# --- Ejecución ---
if __name__ == "__main__":
    generate_report_auto()
