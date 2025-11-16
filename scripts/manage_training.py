# scripts/manage_training.py
"""
Módulo: manage_training.py
Descripción:
    Gestiona el entrenamiento y reentrenamiento (fine-tuning) del modelo Gemma 2B IT
    usando datasets procesados. Todo el manejo de modelos se realiza mediante
    core.controller.model_manager.
"""

from pathlib import Path
import sys
import torch
from core.controller.data_manager import DataManager
from core.controller.model_manager import ModelManager
from core.utils.logger import init_logger

# --- Paths y configuración ---
BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "datasets" / "processed"
LOG_FILE = BASE_DIR / "data" / "outputs" / "logs" / "manage_training.log"

logger = init_logger("manage_training", LOG_FILE)

def log(message: str, level="info"):
    if level == "info":
        logger.info(message)
    elif level == "warning":
        logger.warning(message)
    elif level == "error":
        logger.error(message)
    print(message)

def run_training(epochs=3, batch_size=32, incremental=False):
    """
    Ejecuta entrenamiento o reentrenamiento usando core/controller.
    
    :param epochs: número de épocas para el fine-tuning.
    :param batch_size: tamaño de batch.
    :param incremental: si True, hace reentrenamiento sobre modelo existente.
    """
    log("=== Iniciando proceso de entrenamiento/reentrenamiento ===")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    log(f"[INFO] Dispositivo seleccionado: {device}")

    # Inicializar core
    data_manager = DataManager()
    model_manager = ModelManager()

    # Verificar datasets procesados
    processed_files = list(PROCESSED_DIR.glob("*.*"))
    if not processed_files:
        log(f"[ERROR] No se encontraron archivos en {PROCESSED_DIR}", level="error")
        sys.exit(1)

    # Iterar sobre todos los datasets
    for file_path in processed_files:
        try:
            log(f"[INFO] Procesando dataset: {file_path.name}")
            df = data_manager.load_data(str(file_path))
            log(f"[INFO] Dataset cargado: {len(df)} registros")

            # Cargar modelo base o fine-tuned según incremental
            if incremental:
                model = model_manager.load_fine_tuned_model()
                log("[INFO] Cargando modelo fine-tuned existente para reentrenamiento")
            else:
                model = model_manager.load_model(version="latest")
                log("[INFO] Cargando modelo base para entrenamiento inicial")

            # Ejecutar fine-tuning
            model_manager.fine_tune(df, epochs=epochs, batch_size=batch_size)
            log("[INFO] Fine-tuning completado exitosamente")

            # Evaluación del modelo
            metrics = model_manager.evaluate_model(metrics=[])
            log(f"[INFO] Evaluación completada. Métricas: {metrics}")

        except Exception as e:
            log(f"[ERROR] Error procesando {file_path.name}: {e}", level="error")
            model_manager.rollback_to_previous_version()
            log("[INFO] Rollback realizado a la versión anterior del modelo")

    log("=== Proceso de entrenamiento/reentrenamiento finalizado ===")

# --- Ejecución ---
if __name__ == "__main__":
    run_training(epochs=3, batch_size=32, incremental=False)
#Solo cambia el parámetro incremental=True 
# para reentrenamiento sobre un modelo fine-tuned existente.