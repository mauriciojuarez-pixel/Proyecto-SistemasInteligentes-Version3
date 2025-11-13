import os
import shutil
from pathlib import Path
from utils.logger import log_info, log_error

def save_checkpoint(trainer, output_dir: str = "models/fine_tuned/checkpoints", version: str = None):
    """
    Guarda un checkpoint del modelo entrenado.
    """
    try:
        version = version or "v1"
        path = Path(output_dir) / version
        trainer.save_model(path)
        log_info(f"Checkpoint del modelo guardado en {path}")
    except Exception as e:
        log_error(f"Error al guardar checkpoint: {e}")
        raise

def list_model_versions(model_dir: str = "models/fine_tuned/checkpoints") -> list:
    """
    Lista las versiones disponibles del modelo fine-tuned.
    """
    try:
        versions = [d for d in os.listdir(model_dir) if os.path.isdir(Path(model_dir) / d)]
        log_info(f"Versiones de modelo encontradas: {versions}")
        return versions
    except Exception as e:
        log_error(f"Error al listar versiones del modelo: {e}")
        raise

def load_checkpoint(version: str, model_dir: str = "models/fine_tuned/checkpoints"):
    """
    Carga un checkpoint específico del modelo.
    """
    from transformers import AutoModelForCausalLM
    try:
        path = Path(model_dir) / version
        model = AutoModelForCausalLM.from_pretrained(path)
        log_info(f"Modelo cargado desde versión: {version}")
        return model
    except Exception as e:
        log_error(f"Error al cargar modelo versión {version}: {e}")
        raise

def delete_old_models(model_dir: str = "models/fine_tuned/checkpoints", keep_last: int = 3):
    """
    Elimina checkpoints antiguos manteniendo solo los N más recientes.
    """
    try:
        dirs = sorted(Path(model_dir).iterdir(), key=os.path.getmtime, reverse=True)
        for old in dirs[keep_last:]:
            shutil.rmtree(old)
            log_info(f"Modelo antiguo eliminado: {old}")
    except Exception as e:
        log_error(f"Error al eliminar modelos antiguos: {e}")
        raise
