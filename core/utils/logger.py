import logging
from pathlib import Path
from datetime import datetime

def init_logger(name: str, log_file: Path = None):
    """Inicializa logger con consola y archivo"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')

        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        if log_file is None:
            log_file = Path("data/outputs/logs") / f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
        log_file.parent.mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(log_file, encoding='utf-8')
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger

def log_info(logger, message: str):
    logger.info(message)

def log_warning(logger, message: str):
    logger.warning(message)

def log_error(logger, message: str):
    logger.error(message)

def save_log(logger):
    for handler in logger.handlers:
        if hasattr(handler, 'flush'):
            handler.flush()
