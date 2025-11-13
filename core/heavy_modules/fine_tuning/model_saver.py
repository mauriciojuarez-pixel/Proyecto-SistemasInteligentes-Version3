# core/heavy_modules/fine_tuning/model_saver.py

import os
import shutil
from pathlib import Path
from core.utils.logger import init_logger, log_info, log_error

logger = init_logger("ModelSaver")


def save_checkpoint(trainer, output_dir: str = "models/fine_tuned/checkpoints", version: str = None):
    """
    Guarda un checkpoint del modelo entrenado.
    """
    try:
        version = version or "v1"
        path = Path(output_dir) / version
        path.mkdir(parents=True, exist_ok=True)
        trainer.save_model(path)
        log_info(logger, f"Checkpoint del modelo guardado en {path}")
    except Exception as e:
        log_error(logger, f"Error al guardar checkpoint: {e}")
        raise


def list_model_versions(model_dir: str = "models/fine_tuned/checkpoints") -> list:
    """
    Lista las versiones disponibles del modelo fine-tuned.
    """
    try:
        versions = [d.name for d in Path(model_dir).iterdir() if d.is_dir()]
        log_info(logger, f"Versiones de modelo encontradas: {versions}")
        return versions
    except Exception as e:
        log_error(logger, f"Error al listar versiones del modelo: {e}")
        raise


def load_checkpoint(version: str, model_dir: str = "models/fine_tuned/checkpoints"):
    """
    Carga un checkpoint específico del modelo.
    """
    from transformers import AutoModelForCausalLM
    try:
        path = Path(model_dir) / version
        model = AutoModelForCausalLM.from_pretrained(path)
        log_info(logger, f"Modelo cargado desde versión: {version}")
        return model
    except Exception as e:
        log_error(logger, f"Error al cargar modelo versión {version}: {e}")
        raise


def delete_old_models(model_dir: str = "models/fine_tuned/checkpoints", keep_last: int = 3):
    """
    Elimina checkpoints antiguos manteniendo solo los N más recientes.
    """
    try:
        dirs = sorted(Path(model_dir).iterdir(), key=lambda d: d.stat().st_mtime, reverse=True)
        for old in dirs[keep_last:]:
            if old.is_dir():
                shutil.rmtree(old)
                log_info(logger, f"Modelo antiguo eliminado: {old}")
    except Exception as e:
        log_error(logger, f"Error al eliminar modelos antiguos: {e}")
        raise
