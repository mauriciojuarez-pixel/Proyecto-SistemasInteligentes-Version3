# core/controller/report_manager.py

import os
from datetime import datetime
import pandas as pd
from core.utils.logger import log_info, log_error
from core.heavy_modules.reporting.report_builder import ReportBuilder

REPORT_DIR = "reports/"


class ReportManager:
    """
    Supervisa la generación completa del reporte (texto, gráficos, métricas y conclusiones).
    Cada función documentada corresponde a un método público.
    """

    def __init__(self):
        if not os.path.exists(REPORT_DIR):
            os.makedirs(REPORT_DIR)
        self.builder = ReportBuilder()
        self.visualizations = []

    # ---------------------------------------------------------------
    # 1. Generar reporte completo
    # ---------------------------------------------------------------
    def generate_report(self, data: pd.DataFrame, insights: dict, model_results: dict = None):
        """
        Crea un reporte a partir de los resultados del análisis.
        data: DataFrame principal
        insights: dict con secciones de texto
        model_results: dict opcional con resultados de modelo para métricas
        """
        try:
            self.builder.build_structure()
            self.builder.add_text_sections(insights)
            if model_results:
                self.builder.insert_metrics(model_results)
            log_info("Reporte generado correctamente.")
            return self.builder.report
        except Exception as e:
            log_error(f"Error generando el reporte: {e}")
            raise

    # ---------------------------------------------------------------
    # 2. Generar gráficos y visualizaciones
    # ---------------------------------------------------------------
    def add_visualizations(self, chart_paths: list):
        """
        Genera gráficos y visualizaciones.
        chart_paths: lista de rutas de imágenes o gráficos generados
        """
        try:
            self.builder.embed_charts(chart_paths)
            self.visualizations.extend(chart_paths)
            log_info(f"{len(chart_paths)} visualizaciones agregadas al reporte.")
        except Exception as e:
            log_error(f"Error agregando visualizaciones: {e}")
            raise

    # ---------------------------------------------------------------
    # 3. Compilar secciones del reporte
    # ---------------------------------------------------------------
    def compile_sections(self, analysis: dict, graphs: list, summary: dict):
        """
        Une los distintos componentes (texto, métricas, figuras) en el reporte.
        """
        try:
            self.builder.add_text_sections(analysis)
            self.builder.embed_charts(graphs)
            if summary:
                self.builder.insert_metrics(summary)
            log_info("Secciones compiladas correctamente.")
            return self.builder.report
        except Exception as e:
            log_error(f"Error compilando secciones: {e}")
            raise

    # ---------------------------------------------------------------
    # 4. Exportar a PDF
    # ---------------------------------------------------------------
    def export_to_pdf(self, filename: str = None):
        """
        Exporta el reporte final a PDF.
        """
        try:
            if filename is None:
                filename = os.path.join(REPORT_DIR, self.auto_name_report("pdf"))
            self.builder.finalize_report(export_format="pdf", filename=filename.replace(".pdf", ""))
            log_info(f"Reporte exportado a PDF: {filename}")
            return filename
        except Exception as e:
            log_error(f"Error exportando PDF: {e}")
            raise

    # ---------------------------------------------------------------
    # 5. Exportar a Excel
    # ---------------------------------------------------------------
    def export_to_excel(self, filename: str = None):
        """
        Exporta el reporte final a Excel.
        """
        try:
            if filename is None:
                filename = os.path.join(REPORT_DIR, self.auto_name_report("xlsx"))
            self.builder.finalize_report(export_format="excel", filename=filename.replace(".xlsx", ""))
            log_info(f"Reporte exportado a Excel: {filename}")
            return filename
        except Exception as e:
            log_error(f"Error exportando Excel: {e}")
            raise

    # ---------------------------------------------------------------
    # 6. Agregar metadata
    # ---------------------------------------------------------------
    def append_metadata(self, info: dict):
        """
        Añade metadatos del modelo, dataset y ejecución al reporte.
        """
        try:
            self.builder.report["metadata"].update(info)
            log_info("Metadata agregada al reporte.")
        except Exception as e:
            log_error(f"Error agregando metadata: {e}")
            raise

    # ---------------------------------------------------------------
    # 7. Nombre automático del archivo
    # ---------------------------------------------------------------
    def auto_name_report(self, ext: str = "pdf"):
        """
        Genera automáticamente el nombre del archivo de salida.
        """
        return f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
