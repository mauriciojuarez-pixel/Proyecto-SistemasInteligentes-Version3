# test/test_scripts_integration.py
# python -m test.test_scripts_integration
"""
Test de integración del flujo completo actualizado:
1. Limpieza automática de datasets crudos.
2. Procesamiento y carga de datasets.
3. Análisis con AutonomousAgent.
4. Generación de resumen usando PromptBuilder.
5. Creación de reportes PDF y Excel.
"""

from pathlib import Path
import pandas as pd

from core.controller.data_manager import DataManager
from core.controller.report_manager import ReportManager
from core.heavy_modules.agents.autonomous_agent import AutonomousAgent

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
        if df_clean.empty:
            log(f"[WARN] Dataset procesado {f.name} está vacío tras limpieza.")
        data_manager.save_processed(df_clean, f.name)
        log(f"[INFO] Dataset procesado: {f.name}")
    return True

def test_integration_flow():
    """Ejecuta el flujo completo de prueba de integración usando AutonomousAgent"""
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

    df_list = [data_manager.load_data(str(f)) for f in files]
    df = pd.concat(df_list, ignore_index=True)
    log(f"[INFO] {len(df)} filas cargadas desde {len(files)} archivos procesados.")

    if df.empty:
        log("[WARN] DataFrame combinado está vacío. Se generará reporte con mensaje por defecto.")

    # 3. Inicializar agente autónomo
    agent = AutonomousAgent(session_id="test_session")

    # 4. Analizar datos con el agente
    analysis = agent.analyze_data(df) if not df.empty else None
    log("[INFO] Análisis de datos completado.")

    # 5. Generar resumen usando PromptBuilder y modelo local
    summary = agent.generate_summary({"analysis": analysis}) if analysis else ""
    if not summary.strip():
        summary = "No se generó resumen debido a datos insuficientes."
    log(f"[INFO] Resumen generado: {summary[:200]}...")  # Mostrar solo inicio

    # 6. Generar reporte final
    report_manager = ReportManager()
    report_manager.append_metadata({
        "autor": "Test Integration",
        "filas": len(df),
        "columnas": list(df.columns),
        "resumen": summary
    })

    # Asegurarse de que haya al menos una sección
    sections = {"Resumen automático": summary} if summary else {"Resumen automático": "No hay contenido disponible."}
    report_manager.generate_report(df, sections)

    pdf_file = report_manager.export_to_pdf()
    excel_file = report_manager.export_to_excel()
    
    log(f"[INFO] Test completado. Reportes generados: PDF -> {pdf_file}, Excel -> {excel_file}")

if __name__ == "__main__":
    test_integration_flow()
