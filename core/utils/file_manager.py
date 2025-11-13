#core/utils/file_manager.py
from pathlib import Path
import pandas as pd

def validate_path(path: Path, create: bool = False) -> bool:
    """Valida que el path exista; opcionalmente lo crea"""
    if create:
        path.mkdir(parents=True, exist_ok=True)
    return path.exists()

def load_csv(file_path: Path) -> pd.DataFrame:
    """Carga un archivo CSV en un DataFrame"""
    if not file_path.exists():
        raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
    return pd.read_csv(file_path)

def load_excel(file_path: Path) -> pd.DataFrame:
    """Carga un archivo Excel en un DataFrame"""
    if not file_path.exists():
        raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
    return pd.read_excel(file_path)

def save_file(df: pd.DataFrame, file_path: Path, index=False):
    """Guarda DataFrame en CSV o Excel según extensión"""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    if file_path.suffix.lower() == ".csv":
        df.to_csv(file_path, index=index)
    elif file_path.suffix.lower() in [".xls", ".xlsx"]:
        df.to_excel(file_path, index=index)
    else:
        raise ValueError(f"Extensión no soportada: {file_path.suffix}")

def get_filename(file_path: Path) -> str:
    """Obtiene solo el nombre del archivo sin extensión"""
    return file_path.stem
