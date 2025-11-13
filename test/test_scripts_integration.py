# test/test_scripts_integration.py
# python -m test.test_scripts_integration
"""
Test de integración del flujo completo:
1. Limpieza automática de datasets crudos.
2. Procesamiento y carga de datasets.
3. Generación de reporte PDF y Excel usando ReportManager.
"""

from pathlib import Path
import shutil
import sys
import pandas as pd

from core.controller.data_manager import DataManager
from core.controller.report_manager import ReportManager

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data/datasets/raw"
PROCESSED_DIR = BASE_DIR / "data/datasets/processed"
REPORTS_DIR = BASE_DIR / "data/outputs/reports"

def log(msg):
    print(msg)

def prepare_processed_data():
    """Procesa automáticamente los datasets crudos y los guarda en processed/"""
    data_manager = DataManager()
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    log("=== Preparando datasets procesados a partir de raw/ ===")
    
    raw_files = list(RAW_DIR.glob("*.*"))
    if not raw_files:
        log("[WARN] No hay archivos crudos en raw/.")
        return False

    for f in raw_files:
        df = data_manager.load_data(str(f))
        df_clean = data_manager.clean_data(df)
        data_manager.save_processed(df_clean, f.name)
        log(f"[INFO] Dataset procesado: {f.name}")
    return True

def test_integration_flow():
    """Ejecuta el flujo completo de prueba de integración"""
    log("=== INICIANDO TEST DE INTEGRACIÓN ===")
    
    # 1. Preparar datasets procesados
    success = prepare_processed_data()
    if not success:
        log("[ERROR] No se pudieron procesar datasets crudos. Test abortado.")
        return
    
    # 2. Cargar archivos procesados
    data_manager = DataManager()
    files = list(PROCESSED_DIR.glob("*.*"))
    assert files, "No se encontraron archivos procesados para el test"

    df_list = []
    for f in files:
        df_list.append(data_manager.load_data(str(f)))
    df = pd.concat(df_list, ignore_index=True)
    log(f"[INFO] {len(df)} filas cargadas desde {len(files)} archivos procesados.")

    # 3. Generar reporte
    report_manager = ReportManager()
    summary = df.describe(include="all").to_dict()
    report_manager.append_metadata({
        "autor": "Test Integration",
        "filas": len(df),
        "columnas": list(df.columns),
        "resumen": summary
    })
    
    insights = {"Conclusión automática": "Resultados generados por Gemma 2B IT (test)."}
    report_manager.generate_report(df, insights)

    pdf_file = report_manager.export_to_pdf()
    excel_file = report_manager.export_to_excel()
    
    log(f"[INFO] Test completado. Reportes generados: PDF -> {pdf_file}, Excel -> {excel_file}")

if __name__ == "__main__":
    test_integration_flow()
