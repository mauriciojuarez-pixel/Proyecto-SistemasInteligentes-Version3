# core/heavy_modules/fine_tuning/data_preparation.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.utils import resample
from transformers import AutoTokenizer
from core.utils.logger import init_logger, log_info, log_error
from core.utils.data_cleaner import remove_nulls, normalize_columns

logger = init_logger("DataPreparation")


def clean_training_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia el dataset de entrenamiento:
    - Elimina valores nulos.
    - Normaliza nombres de columnas.
    - Elimina duplicados.
    """
    try:
        df = remove_nulls(df)
        df = df.drop_duplicates()
        df = normalize_columns(df)
        log_info(logger, f"Datos de entrenamiento limpiados: {df.shape[0]} filas.")
        return df
    except Exception as e:
        log_error(logger, f"Error al limpiar datos de entrenamiento: {e}")
        raise


def tokenize_texts(df: pd.DataFrame, text_col: str, tokenizer_name: str = "google/gemma-2b-it", max_length: int = 128):
    """
    Tokeniza textos para el modelo Gemma.
    Devuelve un diccionario con input_ids y attention_mask.
    """
    try:
        tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
        tokens = tokenizer(
            df[text_col].tolist(),
            truncation=True,
            padding="max_length",
            max_length=max_length,
            return_tensors="pt"
        )
        log_info(logger, f"Textos tokenizados correctamente con {tokenizer_name}.")
        return tokens
    except Exception as e:
        log_error(logger, f"Error al tokenizar textos: {e}")
        raise


def balance_classes(df: pd.DataFrame, label_col: str) -> pd.DataFrame:
    """
    Equilibra las clases mediante sobremuestreo (oversampling).
    """
    try:
        class_counts = df[label_col].value_counts()
        max_count = class_counts.max()

        balanced_df = pd.concat([
            resample(df[df[label_col] == cls],
                     replace=True,
                     n_samples=max_count,
                     random_state=42)
            for cls in class_counts.index
        ])
        log_info(logger, f"Datos balanceados por clase. Total: {balanced_df.shape[0]} registros.")
        return balanced_df.sample(frac=1, random_state=42).reset_index(drop=True)
    except Exception as e:
        log_error(logger, f"Error al balancear clases: {e}")
        raise


def split_train_test(df: pd.DataFrame, test_size: float = 0.2, random_state: int = 42):
    """
    Divide el dataset en conjuntos de entrenamiento y prueba.
    """
    try:
        train_df, test_df = train_test_split(df, test_size=test_size, random_state=random_state)
        log_info(logger, f"Dataset dividido: {len(train_df)} train / {len(test_df)} test.")
        return train_df, test_df
    except Exception as e:
        log_error(logger, f"Error al dividir train/test: {e}")
        raise
