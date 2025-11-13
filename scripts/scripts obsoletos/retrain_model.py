# scripts/retrain_model.py
"""
Módulo: retrain_model.py
Descripción:
    Reentrena (fine-tuning) el modelo Gemma 2B IT usando datasets procesados.
    Todo el manejo del modelo (carga, fine-tuning, evaluación, checkpoints)
    se realiza mediante core.controller.model_manager y core.controller.data_manager.
"""

from pathlib import Path
import sys
import torch
from core.controller.data_manager import DataManager
from core.controller.model_manager import ModelManager
from core.utils.logger.logger import init_logger

# --- Paths y configuración ---
BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DATA_DIR = BASE_DIR / "data" / "datasets" / "processed"
LOG_FILE = BASE_DIR / "data" / "outputs" / "logs" / "retrain_model.log"

logger = init_logger("retrain_model", LOG_FILE)

def log(message: str, level="info"):
    if level == "info":
        logger.info(message)
    elif level == "warning":
        logger.warning(message)
    elif level == "error":
        logger.error(message)
    print(message)

def retrain_model(epochs=3):
    """Reentrenamiento completo del modelo Gemma 2B IT usando core/controller."""

    log("=== Iniciando reentrenamiento de Gemma 2B IT ===")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    log(f"[INFO] Dispositivo seleccionado: {device}")

    # --- Inicializar core ---
    data_manager = DataManager()
    model_manager = ModelManager()

    # --- 1. Preparar datasets ---
    try:
        datasets = list(PROCESSED_DATA_DIR.glob("*.*"))
        if not datasets:
            raise FileNotFoundError(f"No se encontraron datasets en {PROCESSED_DATA_DIR}")

        # Cargar y validar dataset
        df = data_manager.load_data(str(datasets[0]))
        log(f"[INFO] Dataset cargado: {len(df)} registros")

    except Exception as e:
        log(f"[ERROR] Error cargando o preparando datos: {e}", level="error")
        sys.exit(1)

    # --- 2. Cargar modelo y fine-tuning ---
    try:
        model = model_manager.load_model(version='latest')
        log("[INFO] Modelo cargado correctamente.")

        # Ejecutar fine-tuning
        model_manager.fine_tune(df, epochs=epochs)
        log("[INFO] Fine-tuning completado con éxito.")

    except Exception as e:
        log(f"[ERROR] Error durante el fine-tuning: {e}", level="error")
        model_manager.rollback_to_previous_version()
        sys.exit(1)

    # --- 3. Evaluación ---
    try:
        metrics = model_manager.evaluate_model(metrics=[])
        log(f"[INFO] Evaluación completada. Métricas: {metrics}")

    except Exception as e:
        log(f"[ERROR] Error evaluando el modelo: {e}", level="error")

    # --- 4. Guardar checkpoint ---
    try:
        checkpoint_name = f"gemma_finetuned_{len(df)}_{device}"
        model_manager.save_model_checkpoint(name=checkpoint_name)
        log(f"[INFO] Modelo fine-tuned y checkpoint guardados: {checkpoint_name}")

    except Exception as e:
        log(f"[ERROR] Error guardando el modelo: {e}", level="error")

    log("=== Reentrenamiento finalizado ===")

# --- Ejecución ---
if __name__ == "__main__":
    retrain_model(epochs=3)
