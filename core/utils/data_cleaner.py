#core/utils/data_cleaner.py
import pandas as pd
from pathlib import Path
from scipy.stats import zscore

def remove_nulls(df: pd.DataFrame, strategy="mean") -> pd.DataFrame:
    """Rellena valores nulos en columnas numéricas"""
    for col in df.select_dtypes(include='number').columns:
        if strategy == "mean":
            df[col].fillna(df[col].mean(), inplace=True)
        elif strategy == "median":
            df[col].fillna(df[col].median(), inplace=True)
    return df

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Elimina filas duplicadas"""
    return df.drop_duplicates()

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza nombres de columnas (lowercase + sin espacios)"""
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    return df

def detect_noise(df: pd.DataFrame, z_thresh=3) -> pd.DataFrame:
    """Elimina outliers usando Z-score"""
    numeric_cols = df.select_dtypes(include='number').columns
    return df[(df[numeric_cols].apply(zscore).abs() < z_thresh).all(axis=1)]

def save_clean_data(df: pd.DataFrame, path: Path, index=False):
    """Guarda datos limpios (CSV o Excel)"""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix.lower() == ".csv":
        df.to_csv(path, index=index)
    else:
        df.to_excel(path, index=index)
