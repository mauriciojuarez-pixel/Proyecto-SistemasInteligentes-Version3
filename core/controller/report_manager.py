# core/controller/report_manager.py

from pathlib import Path
import os
from datetime import datetime
import pandas as pd
from core.utils.logger import init_logger, log_info, log_error
from core.heavy_modules.reporting.report_builder import ReportBuilder
from core.utils.prompt_builder import BuilderPrompt
from core.controller.model_manager import ModelManager

REPORT_DIR = "reports/"

# Inicializar logger central del ReportManager
logger = init_logger("ReportManager", Path(REPORT_DIR) / "report_manager.log")


class ReportManager:
    """
    Administra la generación de reportes, incluyendo textos interpretativos,
    métricas del modelo y visualizaciones.
    """

    def __init__(self):
        os.makedirs(REPORT_DIR, exist_ok=True)

        # Componentes del reporte
        self.builder = ReportBuilder()  # No se pasa logger
        self.visualizations = []
        self.prompt_builder = BuilderPrompt()
        self.model_manager = ModelManager()

    # ---------------------------------------------------------------
    # Generación de texto interpretativo con el modelo Gemma
    # ---------------------------------------------------------------
    def generate_interpretative_text(self, data: pd.DataFrame) -> str:
        try:
            prompt = self.prompt_builder.build_report_prompt(data)
            self.model_manager.load_fine_tuned_model()
            response = self.model_manager.generate_from_prompt(prompt)
            log_info(logger, "Texto interpretativo generado correctamente por el modelo.")
            return response
        except Exception as e:
            log_error(logger, f"Error generando texto interpretativo: {e}")
            return "No se pudo generar el texto interpretativo."

    # ---------------------------------------------------------------
    # Generación principal de reporte
    # ---------------------------------------------------------------
def generate_report(self, data: pd.DataFrame, model_results: dict = None):
    try:
        # 1. PRIMERO: Generar el texto interpretativo usando el modelo
        log_info(logger, "Generando texto interpretativo con el modelo...")
        interpretative_text = self.generate_interpretative_text(data)
        
        # 2. SEGUNDO: Crear el diccionario de insights con el RESULTADO del modelo
        insights = {
            "Análisis Interpretativo": interpretative_text,
            "Fecha de Análisis": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # 3. TERCERO: Construir el reporte con los resultados procesados
        self.builder.build_structure()
        self.builder.add_text_sections(insights)  # Ahora insights contiene el RESULTADO, no el prompt
        
        if model_results:
            self.builder.insert_metrics(model_results)
            
        log_info(logger, "Reporte generado correctamente.")
        return self.builder.report
    except Exception as e:
        log_error(logger, f"Error generando el reporte: {e}")
        raise

    # ---------------------------------------------------------------
    # Visualizaciones y secciones
    # ---------------------------------------------------------------
    def add_visualizations(self, chart_paths: list):
        try:
            self.builder.embed_charts(chart_paths)
            self.visualizations.extend(chart_paths)
            log_info(logger, f"{len(chart_paths)} visualizaciones agregadas al reporte.")
        except Exception as e:
            log_error(logger, f"Error agregando visualizaciones: {e}")
            raise

    def compile_sections(self, analysis: dict, graphs: list, summary: dict):
        try:
            self.builder.add_text_sections(analysis)
            self.builder.embed_charts(graphs)
            if summary:
                self.builder.insert_metrics(summary)
            log_info(logger, "Secciones compiladas correctamente.")
            return self.builder.report
        except Exception as e:
            log_error(logger, f"Error compilando secciones: {e}")
            raise

    # ---------------------------------------------------------------
    # Exportación
    # ---------------------------------------------------------------
    def export_to_pdf(self, filename: str = None):
        try:
            if filename is None:
                filename = os.path.join(REPORT_DIR, self.auto_name_report("pdf"))
            self.builder.finalize_report(export_format="pdf", filename=filename.replace(".pdf", ""))
            log_info(logger, f"Reporte exportado a PDF: {filename}")
            return filename
        except Exception as e:
            log_error(logger, f"Error exportando PDF: {e}")
            raise

    def export_to_excel(self, filename: str = None):
        try:
            if filename is None:
                filename = os.path.join(REPORT_DIR, self.auto_name_report("xlsx"))
            self.builder.finalize_report(export_format="excel", filename=filename.replace(".xlsx", ""))
            log_info(logger, f"Reporte exportado a Excel: {filename}")
            return filename
        except Exception as e:
            log_error(logger, f"Error exportando Excel: {e}")
            raise

    # ---------------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------------
    def append_metadata(self, info: dict):
        try:
            self.builder.report["metadata"].update(info)
            log_info(logger, "Metadata agregada al reporte.")
        except Exception as e:
            log_error(logger, f"Error agregando metadata: {e}")
            raise

    # ---------------------------------------------------------------
    # Nombre automático de reportes
    # ---------------------------------------------------------------
    def auto_name_report(self, ext: str = "pdf"):
        return f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
