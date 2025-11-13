# core/utils/logger.py

import logging
from pathlib import Path
from datetime import datetime

def init_logger(name: str, log_file=None):
    """
    Inicializa un logger con salida a consola y a archivo.
    log_file: str o Path, opcional. Si no se provee, se crea en data/outputs/logs/
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        # Formato de logs
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')

        # Consola
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        # Archivo
        if log_file is None:
            log_file = Path("data/outputs/logs") / f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
        else:
            log_file = Path(log_file)  # Convertir str a Path si es necesario

        # Crear directorio si no existe
        log_file.parent.mkdir(parents=True, exist_ok=True)

        fh = logging.FileHandler(log_file, encoding='utf-8')
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger

# Funciones auxiliares para usar el logger
def log_info(logger, message: str):
    logger.info(message)

def log_warning(logger, message: str):
    logger.warning(message)

def log_error(logger, message: str):
    logger.error(message)
