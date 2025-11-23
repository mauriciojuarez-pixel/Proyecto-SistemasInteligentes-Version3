# core/heavy_modules/reporting/report_builder.py

from datetime import datetime
from core.heavy_modules.reporting import export_pdf, export_excel
from core.heavy_modules.reporting.metrics import evaluate_model_performance, summarize_results
from core.utils.logger import init_logger, log_info, log_warning, log_error

class ReportBuilder:
    """
    Construye y exporta reportes combinando texto, métricas y visualizaciones.
    Soporta PDF y Excel, con logging y validaciones.
    """

    def __init__(self, title: str = "Reporte Técnico de IA"):
        self.logger = init_logger("ReportBuilder")
        self.report = {
            "title": title,
            "sections": {},   # Aquí se guardarán los textos
            "charts": [],
            "metrics": {},
            "metadata": {}
        }
        log_info(self.logger, f"ReportBuilder inicializado: {title}")

    # ---------------------------------------------------------------
    # Construcción de la estructura del reporte
    # ---------------------------------------------------------------
    def build_structure(self, metadata: dict = None):
        """Inicializa metadata básica del reporte."""
        try:
            self.report["metadata"] = metadata or {
                "autor": "Sistema Inteligente",
                "versión": "1.0",
                "fecha_creacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            log_info(self.logger, "Estructura del reporte construida correctamente.")
            return self.report
        except Exception as e:
            log_error(self.logger, f"Error construyendo estructura del reporte: {e}")
            raise

    # ---------------------------------------------------------------
    # Agregar secciones de texto
    # ---------------------------------------------------------------
    def add_text_sections(self, sections: dict):
        """Agrega texto generado por el modelo al reporte."""
        try:
            if not isinstance(sections, dict):
                raise TypeError("sections debe ser un diccionario {titulo: contenido}.")
            self.report["sections"].update(sections)
            log_info(self.logger, f"Se agregaron {len(sections)} secciones al reporte.")
        except Exception as e:
            log_error(self.logger, f"Error agregando secciones: {e}")
            raise

    # ---------------------------------------------------------------
    # Incrustar gráficos
    # ---------------------------------------------------------------
    def embed_charts(self, chart_paths: list):
        try:
            if not isinstance(chart_paths, list):
                raise TypeError("chart_paths debe ser una lista de rutas de archivos.")
            self.report["charts"].extend(chart_paths)
            log_info(self.logger, f"Se incrustaron {len(chart_paths)} gráficos en el reporte.")
        except Exception as e:
            log_error(self.logger, f"Error al incrustar gráficos: {e}")
            raise

    # ---------------------------------------------------------------
    # Insertar métricas y resumen de modelo
    # ---------------------------------------------------------------
    def insert_metrics(self, model_results: dict):
        try:
            if not model_results:
                log_warning(self.logger, "No se proporcionaron resultados del modelo; las métricas serán vacías.")
                self.report["metrics"] = {}
                self.add_text_sections({"Resumen de métricas": "No se generaron métricas."})
                return

            metrics = evaluate_model_performance(model_results)
            summary = summarize_results(metrics)
            self.report["metrics"] = metrics
            self.add_text_sections({"Resumen de métricas": summary})
            log_info(self.logger, "Métricas insertadas correctamente en el reporte.")
        except Exception as e:
            log_error(self.logger, f"Error insertando métricas: {e}")
            raise

    # ---------------------------------------------------------------
    # Agregar resumen del análisis o modelo
    # ---------------------------------------------------------------
    def add_model_summary(self, title: str, text: str):
        """Agrega el resumen generado por el modelo al reporte."""
        try:
            if not text:
                log_warning(self.logger, f"No se proporcionó texto para la sección '{title}'.")
                return
            self.add_text_sections({title: text})
            log_info(self.logger, f"Resumen '{title}' agregado correctamente al reporte.")
        except Exception as e:
            log_error(self.logger, f"Error agregando resumen '{title}': {e}")
            raise

    # ---------------------------------------------------------------
    # Finalizar y exportar reporte
    # ---------------------------------------------------------------
    def finalize_report(self, export_format="pdf", filename: str = "reporte_final"):
        try:
            formats = [export_format] if isinstance(export_format, str) else export_format
            if not formats:
                raise ValueError("Debe proporcionar al menos un formato de exportación válido.")

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            for fmt in formats:
                file_with_ts = f"{filename}_{timestamp}"
                if fmt.lower() == "pdf":
                    export_pdf.create_pdf(self.report, f"{file_with_ts}.pdf")
                elif fmt.lower() == "excel":
                    export_excel.create_excel_summary(self.report, f"{file_with_ts}.xlsx")
                else:
                    log_warning(self.logger, f"Formato no soportado: {fmt}. Se ignorará.")

            log_info(self.logger, f"Reporte exportado exitosamente en: {', '.join([f.upper() for f in formats])}")
        except Exception as e:
            log_error(self.logger, f"Error finalizando reporte: {e}")
            raise
