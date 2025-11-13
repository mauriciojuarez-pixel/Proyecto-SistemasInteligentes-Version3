# core/controller/data_manager.py

import json
from pathlib import Path
from typing import Tuple
import pandas as pd
from jsonschema import ValidationError

from core.utils.data_cleaner import (
    remove_nulls,
    remove_duplicates,
    normalize_columns,
    detect_noise,
    save_clean_data
)
from core.utils.logger import init_logger, log_info, log_warning, log_error

# Inicializar logger central
logger = init_logger("DataManager")

# Carpeta para datos procesados
PROCESSED_DIR = Path("data/datasets/processed/")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


class DataManager:
    """
    Gestiona los archivos cargados por el usuario (Excel/CSV),
    asegurando su validez, limpieza y compatibilidad con los análisis.
    """

    def __init__(self, schema_path: str = "config/data_schema.json"):
        self.schema_path = Path(schema_path)
        self.processed_dir = PROCESSED_DIR

    # ---------------------------------------------------------------
    # 1. Detectar tipo de archivo
    # ---------------------------------------------------------------
    def detect_file_type(self, file_path: str) -> str:
        if file_path.endswith(".csv"):
            return "csv"
        elif file_path.endswith(".xlsx") or file_path.endswith(".xls"):
            return "excel"
        else:
            raise ValueError("Tipo de archivo no soportado. Solo CSV o Excel.")

    # ---------------------------------------------------------------
    # 2. Cargar datos
    # ---------------------------------------------------------------
    def load_data(self, file_path: str) -> pd.DataFrame:
        file_type = self.detect_file_type(file_path)
        log_info(logger, f"Cargando dataset desde {file_path} ({file_type})")
        try:
            df = pd.read_csv(file_path) if file_type == "csv" else pd.read_excel(file_path)
        except Exception as e:
            log_error(logger, f"Error al cargar el archivo: {e}")
            raise RuntimeError(f"No se pudo cargar el archivo: {e}")
        return df

    # ---------------------------------------------------------------
    # 3. Validación de estructura
    # ---------------------------------------------------------------
    def validate_structure(self, df: pd.DataFrame) -> bool:
        try:
            if not self.schema_path.exists():
                log_warning(logger, "Archivo de esquema no encontrado. Se omitirá la validación.")
                return True

            with open(self.schema_path, "r", encoding="utf-8") as f:
                schema = json.load(f)

            expected_columns = schema.get("columns", [])
            missing_cols = [col for col in expected_columns if col not in df.columns]
            if missing_cols:
                log_error(logger, f"Columnas faltantes: {missing_cols}")
                raise ValidationError(f"Columnas faltantes: {missing_cols}")

            log_info(logger, "Estructura del dataset validada correctamente.")
            return True
        except Exception as e:
            log_error(logger, f"Error validando estructura: {e}")
            raise

    # ---------------------------------------------------------------
    # 4. Limpieza y preprocesamiento
    # ---------------------------------------------------------------
    def clean_data(self, df: pd.DataFrame, fill_strategy="mean", remove_outliers=True) -> pd.DataFrame:
        log_info(logger, "Iniciando limpieza de datos...")
        df = normalize_columns(df)
        df = remove_nulls(df, strategy=fill_strategy)
        df = remove_duplicates(df)
        if remove_outliers:
            df = detect_noise(df)
        log_info(logger, "Limpieza completada.")
        return df

    # ---------------------------------------------------------------
    # 5. División de datos
    # ---------------------------------------------------------------
    def split_data(self, df: pd.DataFrame, test_size: float = 0.2) -> Tuple[pd.DataFrame, pd.DataFrame]:
        if df.empty:
            raise ValueError("El DataFrame está vacío, no se puede dividir.")
        split_index = int(len(df) * (1 - test_size))
        train_df = df.iloc[:split_index].reset_index(drop=True)
        val_df = df.iloc[split_index:].reset_index(drop=True)
        log_info(logger, f"Datos divididos: {len(train_df)} entrenamiento, {len(val_df)} validación.")
        return train_df, val_df

    # ---------------------------------------------------------------
    # 6. Guardado de datos procesados
    # ---------------------------------------------------------------
    def save_processed(self, df: pd.DataFrame, filename: str = "processed_data.csv") -> str:
        output_path = self.processed_dir / filename
        save_clean_data(df, output_path)
        log_info(logger, f"Datos procesados guardados en: {output_path}")
        return str(output_path)

    # ---------------------------------------------------------------
    # 7. Resumen del dataset
    # ---------------------------------------------------------------
    def summarize_dataset(self, df: pd.DataFrame) -> dict:
        summary = {
            "rows": len(df),
            "columns": list(df.columns),
            "missing_values": df.isnull().sum().to_dict(),
            "summary_stats": df.describe(include="all").to_dict()
        }
        log_info(logger, "Resumen del dataset generado.")
        return summary
