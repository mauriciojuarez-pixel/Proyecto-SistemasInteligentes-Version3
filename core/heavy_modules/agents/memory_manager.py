#core/heavy_modules/agents/memory_manager.py

import json
from pathlib import Path
from core.utils.logger import init_logger, log_info, log_error

logger = init_logger("MemoryManager")

class MemoryManager:
    def __init__(self, memory_dir="data/outputs/memory"):
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        log_info(logger, "MemoryManager inicializado correctamente.")

    # En todas las funciones, cambiar log_info/log_error por log_info(logger, ...) y log_error(logger, ...)


    def _get_memory_file(self, session_id):
        return self.memory_dir / f"{session_id}.json"

    def store_context(self, session_id, info: dict):
        """
        Guarda información relevante entre ejecuciones.
        """
        try:
            file = self._get_memory_file(session_id)
            data = {}
            if file.exists():
                with open(file, "r", encoding="utf-8") as f:
                    data = json.load(f)
            data.update(info)
            with open(file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            log_info(f"Contexto guardado para sesión {session_id}.")
        except Exception as e:
            log_error(f"Error al guardar contexto: {e}")
            raise

    def recall_context(self, session_id):
        """
        Recupera contexto previo.
        """
        try:
            file = self._get_memory_file(session_id)
            if not file.exists():
                return {}
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
            log_info(f"Contexto recuperado para sesión {session_id}.")
            return data
        except Exception as e:
            log_error(f"Error al recuperar contexto: {e}")
            raise

    def clear_memory(self, session_id):
        """
        Limpia la memoria asociada a una sesión.
        """
        try:
            file = self._get_memory_file(session_id)
            if file.exists():
                file.unlink()
                log_info(f"Memoria de sesión {session_id} eliminada.")
            else:
                log_info(f"No se encontró memoria para la sesión {session_id}.")
        except Exception as e:
            log_error(f"Error al limpiar memoria: {e}")
            raise
