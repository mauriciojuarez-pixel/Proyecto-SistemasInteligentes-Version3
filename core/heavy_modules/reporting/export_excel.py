# core/heavy_modules/reporting/export_excel.py

import pandas as pd
from core.utils.logger import log_info, log_error


def create_excel_summary(report_data: dict, filename: str):
    """
    Genera un archivo Excel con métricas y secciones del reporte.
    """
    try:
        with pd.ExcelWriter(filename, engine="openpyxl") as writer:
            # Hoja de métricas
            metrics = report_data.get("metrics", {})
            if metrics:
                df_metrics = pd.DataFrame(list(metrics.items()), columns=["Métrica", "Valor"])
                df_metrics.to_excel(writer, sheet_name="Métricas", index=False)

            # Hoja de texto
            sections = report_data.get("sections", {})
            if sections:
                df_text = pd.DataFrame(sections.items(), columns=["Sección", "Contenido"])
                df_text.to_excel(writer, sheet_name="Secciones", index=False)

        log_info(f"Archivo Excel generado correctamente: {filename}")
    except Exception as e:
        log_error(f"Error generando Excel: {e}")
        raise


def export_sheets(writer: pd.ExcelWriter, sheets: dict):
    """
    Exporta varias hojas a un ExcelWriter ya abierto.
    sheets: dict de {nombre_hoja: DataFrame}
    """
    try:
        for name, df in sheets.items():
            df.to_excel(writer, sheet_name=name, index=False)
        log_info(f"{len(sheets)} hojas exportadas correctamente.")
    except Exception as e:
        log_error(f"Error exportando hojas: {e}")
        raise


def save_excel(writer: pd.ExcelWriter, filename: str):
    """
    Guarda el ExcelWriter en un archivo.
    """
    try:
        writer.close()
        log_info(f"Archivo Excel guardado correctamente: {filename}")
    except Exception as e:
        log_error(f"Error guardando Excel: {e}")
        raise
