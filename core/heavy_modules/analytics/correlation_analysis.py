# core/heavy_modules/analytics/correlation_analysis.py

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
from core.utils.logger import init_logger, log_info, log_error
from core.utils.file_manager import validate_path
import numpy as np


logger = init_logger("CorrelationAnalysis")


def compute_correlations(df: pd.DataFrame, method: str = "pearson") -> pd.DataFrame:
    try:
        corr_matrix = df.corr(method=method, numeric_only=True)
        log_info(logger, f"Matriz de correlación ({method}) calculada correctamente.")
        return corr_matrix
    except Exception as e:
        log_error(logger, f"Error al calcular correlaciones: {e}")
        raise


def detect_multicollinearity(df: pd.DataFrame, threshold: float = 0.9) -> list:
    try:
        corr = df.corr(numeric_only=True).abs()
        upper = corr.where(pd.DataFrame(np.triu(np.ones(corr.shape), k=1), index=corr.index, columns=corr.columns).astype(bool))
        high_corr = [(col, row, corr_val)
                     for col in upper.columns
                     for row, corr_val in upper[col].items()
                     if corr_val > threshold]
        log_info(logger, f"Se detectaron {len(high_corr)} pares altamente correlacionados.")
        return high_corr
    except Exception as e:
        log_error(logger, f"Error al detectar multicolinealidad: {e}")
        raise


def visualize_correlation_matrix(corr_matrix: pd.DataFrame, output_file: str = "reports/analytics/correlation_heatmap.png") -> None:
    try:
        output_path = validate_path(Path(output_file).parent)
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f")
        plt.title("Matriz de Correlación")
        plt.tight_layout()
        plt.savefig(output_file)
        plt.close()
        log_info(logger, f"Heatmap de correlación guardado en {output_file}")
    except Exception as e:
        log_error(logger, f"Error al visualizar matriz de correlaciones: {e}")
        raise
