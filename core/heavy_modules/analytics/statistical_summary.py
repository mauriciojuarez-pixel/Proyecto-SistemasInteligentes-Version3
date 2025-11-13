import pandas as pd
import json
import matplotlib.pyplot as plt
from pathlib import Path

from utils.logger import log_info, log_error
from utils.file_manager import validate_path

def compute_descriptive_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula estadísticas descriptivas básicas de columnas numéricas.
    Incluye media, mediana, std, min, max, y cuartiles.
    """
    try:
        desc = df.describe().T
        desc["median"] = df.median(numeric_only=True)
        log_info("Estadísticas descriptivas calculadas correctamente.")
        return desc
    except Exception as e:
        log_error(f"Error al calcular estadísticas descriptivas: {e}")
        raise

def generate_histograms(df: pd.DataFrame, output_dir: str = "reports/analytics/histograms") -> None:
    """
    Genera histogramas automáticos para todas las columnas numéricas.
    Guarda las imágenes en la carpeta especificada.
    """
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
        
        log_info(f"Histogramas generados y guardados en {output_path}")
    except Exception as e:
        log_error(f"Error al generar histogramas: {e}")
        raise

def summary_to_json(summary_df: pd.DataFrame, output_file: str = "reports/analytics/descriptive_stats.json") -> None:
    """
    Convierte el resumen estadístico en formato JSON y lo guarda.
    """
    try:
        output_path = validate_path(Path(output_file).parent)
        summary_json = summary_df.to_dict(orient="index")

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(summary_json, f, indent=4, ensure_ascii=False)
        
        log_info(f"Resumen estadístico exportado correctamente a {output_file}")
    except Exception as e:
        log_error(f"Error al exportar resumen estadístico: {e}")
        raise
