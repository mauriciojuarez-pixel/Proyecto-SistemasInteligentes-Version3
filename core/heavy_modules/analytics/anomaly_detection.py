import pandas as pd
import numpy as np
from scipy.stats import zscore
from utils.logger import log_info, log_error

def detect_outliers(df: pd.DataFrame, method: str = "zscore", threshold: float = 3.0) -> pd.DataFrame:
    """
    Detecta outliers en columnas numéricas usando:
    - Z-score
    - IQR (interquartile range)
    Retorna un DataFrame con una columna adicional 'is_outlier'.
    """
    try:
        df_copy = df.copy()
        numeric_cols = df_copy.select_dtypes(include='number').columns
        
        if method == "zscore":
            z_scores = np.abs(df_copy[numeric_cols].apply(zscore))
            df_copy["is_outlier"] = (z_scores > threshold).any(axis=1)
        elif method == "iqr":
            df_copy["is_outlier"] = False
            for col in numeric_cols:
                Q1 = df_copy[col].quantile(0.25)
                Q3 = df_copy[col].quantile(0.75)
                IQR = Q3 - Q1
                mask = (df_copy[col] < (Q1 - 1.5 * IQR)) | (df_copy[col] > (Q3 + 1.5 * IQR))
                df_copy.loc[mask, "is_outlier"] = True
        else:
            raise ValueError("Método no soportado. Usa 'zscore' o 'iqr'.")
        
        log_info(f"Detección de outliers completada usando método {method}.")
        return df_copy
    except Exception as e:
        log_error(f"Error al detectar outliers: {e}")
        raise

def remove_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    """
    Elimina filas marcadas como outliers.
    """
    try:
        clean_df = df[df.get("is_outlier", False) == False].drop(columns=["is_outlier"], errors="ignore")
        log_info(f"Se eliminaron {len(df) - len(clean_df)} anomalías del dataset.")
        return clean_df
    except Exception as e:
        log_error(f"Error al eliminar anomalías: {e}")
        raise

def flag_noisy_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Marca filas con valores extremos como 'noisy'.
    """
    try:
        df_copy = df.copy()
        numeric_cols = df_copy.select_dtypes(include="number").columns
        df_copy["noisy_score"] = df_copy[numeric_cols].apply(lambda x: np.abs(x - x.mean()) / (x.std() + 1e-8)).mean(axis=1)
        df_copy["is_noisy"] = df_copy["noisy_score"] > 2.5
        log_info("Datos ruidosos etiquetados correctamente.")
        return df_copy
    except Exception as e:
        log_error(f"Error al etiquetar datos ruidosos: {e}")
        raise

def score_data_quality(df: pd.DataFrame) -> float:
    """
    Calcula un puntaje de calidad del dataset en base a proporción de outliers y valores nulos.
    """
    try:
        total_rows = len(df)
        null_ratio = df.isnull().sum().sum() / (total_rows * len(df.columns))
        outlier_ratio = df.get("is_outlier", pd.Series([False]*total_rows)).mean()
        score = max(0, 1 - (null_ratio + outlier_ratio))
        log_info(f"Puntaje de calidad de datos calculado: {score:.3f}")
        return score
    except Exception as e:
        log_error(f"Error al calcular score de calidad de datos: {e}")
        raise
