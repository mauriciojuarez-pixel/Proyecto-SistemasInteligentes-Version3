# core/heavy_modules/analytics/statistical_summary.py

import pandas as pd
import json
import matplotlib.pyplot as plt
from pathlib import Path
from core.utils.logger import init_logger, log_info, log_error
from core.utils.file_manager import validate_path

logger = init_logger("StatSummary")


def compute_descriptive_stats(df: pd.DataFrame) -> pd.DataFrame:
    try:
        desc = df.describe().T
        desc["median"] = df.median(numeric_only=True)
        log_info(logger, "Estadísticas descriptivas calculadas correctamente.")
        return desc
    except Exception as e:
        log_error(logger, f"Error al calcular estadísticas descriptivas: {e}")
        raise


def generate_histograms(df: pd.DataFrame, output_dir: str = "reports/analytics/histograms") -> None:
    try:
        output_path = validate_path(output_dir)
        numeric_cols = df.select_dtypes(include="number").columns

        for col in numeric_cols:
            plt.figure()
            df[col].hist(bins=20, color='steelblue', edgecolor='black')
            plt.title(f"Histograma de {col}")
            plt.xlabel(col)
            plt.ylabel("Frecuencia")
            plt.savefig(Path(output_path) / f"{col}_hist.png")
            plt.close()

        log_info(logger, f"Histogramas generados y guardados en {output_path}")
    except Exception as e:
        log_error(logger, f"Error al generar histogramas: {e}")
        raise


def summary_to_json(summary_df: pd.DataFrame, output_file: str = "reports/analytics/descriptive_stats.json") -> None:
    try:
        output_path = validate_path(Path(output_file).parent)
        summary_json = summary_df.to_dict(orient="index")

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(summary_json, f, indent=4, ensure_ascii=False)

        log_info(logger, f"Resumen estadístico exportado correctamente a {output_file}")
    except Exception as e:
        log_error(logger, f"Error al exportar resumen estadístico: {e}")
        raise
