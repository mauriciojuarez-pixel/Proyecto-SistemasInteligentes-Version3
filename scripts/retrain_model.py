# scripts/retrain_model.py

import sys
from pathlib import Path
from datetime import datetime
import logging
import torch

from core.heavy_modules.fine_tuning.data_preparation import (
    clean_training_data,
    tokenize_texts,
    balance_classes,
    split_train_test
)
from core.heavy_modules.fine_tuning.train_model import (
    initialize_trainer,
    train,
    track_progress,
    log_results
)
from core.heavy_modules.fine_tuning.evaluate_model import (
    compute_metrics,
    compare_with_baseline,
    generate_evaluation_report
)
from core.heavy_modules.fine_tuning.model_saver import (
    save_checkpoint,
    list_model_versions,
    load_checkpoint,
    delete_old_models
)

# --- Configuración de paths ---
BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DATA_DIR = BASE_DIR / "data" / "datasets" / "processed"
FINETUNED_DIR = BASE_DIR / "data" / "models" / "gemma_2b_it_finetuned"
CHECKPOINTS_DIR = BASE_DIR / "data" / "models" / "checkpoints"
LOG_FILE = BASE_DIR / "data" / "outputs" / "logs" / "retrain_model.log"

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
    elif level == "error":
        logging.error(message)
        print(message)
    elif level == "warning":
        logging.warning(message)
        print(message)

def ensure_directories():
    FINETUNED_DIR.mkdir(parents=True, exist_ok=True)
    CHECKPOINTS_DIR.mkdir(parents=True, exist_ok=True)
    log("[INFO] Directorios de fine-tuning y checkpoints verificados/creados.")

def retrain():
    ensure_directories()
    log("=== Iniciando reentrenamiento de Gemma 2B IT ===")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    log(f"[INFO] Se usará dispositivo: {device}")

    # 1. Cargar y preparar datos
    try:
        # Cargar CSV/XLSX procesados
        datasets = list(PROCESSED_DATA_DIR.glob("*.csv")) + list(PROCESSED_DATA_DIR.glob("*.xlsx"))
        if not datasets:
            raise FileNotFoundError(f"No se encontraron datasets en {PROCESSED_DATA_DIR}")

        df = clean_training_data(datasets[0])      # Ejemplo con el primer dataset
        df = tokenize_texts(df)
        df = balance_classes(df)
        train_df, val_df = split_train_test(df)
        log(f"[INFO] Datos cargados y preparados: {len(train_df)} entrenamiento, {len(val_df)} validación")
    except Exception as e:
        log(f"[ERROR] Error cargando/preparando dataset: {e}", level="error")
        sys.exit(1)

    # 2. Inicializar y entrenar
    try:
        trainer = initialize_trainer(train_df, val_df, device=device)
        train(trainer, epochs=3, batch_size=32)
        track_progress(trainer)
        log_results(trainer)
        log("[INFO] Fine-tuning completado con éxito.")
    except Exception as e:
        log(f"[ERROR] Error durante el fine-tuning: {e}", level="error")
        sys.exit(1)

    # 3. Evaluación
    try:
        metrics = compute_metrics(trainer)
        baseline_comparison = compare_with_baseline(metrics)
        evaluation_report = generate_evaluation_report(metrics, baseline_comparison)
        log(f"[INFO] Evaluación completada. Métricas:\n{evaluation_report}")
    except Exception as e:
        log(f"[ERROR] Error evaluando el modelo: {e}", level="error")

    # 4. Guardar modelo
    try:
        save_checkpoint(trainer.model, FINETUNED_DIR, CHECKPOINTS_DIR, name=f"gemma_finetuned_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        log(f"[INFO] Modelo fine-tuned guardado en {FINETUNED_DIR}")
    except Exception as e:
        log(f"[ERROR] Error guardando el modelo: {e}", level="error")

    log("=== Reentrenamiento finalizado ===")

# --- Ejecución ---
if __name__ == "__main__":
    retrain()
