# core/heavy_modules/reporting/report_builder.py

from datetime import datetime
from core.utils.logger import log_info, log_error, log_warning
from core.heavy_modules.reporting import export_pdf, export_excel
from core.heavy_modules.reporting.metrics import evaluate_model_performance, summarize_results


class ReportBuilder:
    """
    Construye y exporta reportes combinando texto, métricas y visualizaciones.
    Robustamente diseñado para soportar PDF y Excel, con logging y validaciones.
    """

    def __init__(self, title: str = "Reporte Técnico de IA"):
        self.report = {
            "title": title,
            "sections": {},
            "charts": [],
            "metrics": {},
            "metadata": {}
        }
        log_info(f"ReportBuilder inicializado: {title}")

    def build_structure(self, metadata: dict = None):
        """Crea la estructura base del reporte con metadatos por defecto si no se proporcionan."""
        try:
            self.report["metadata"] = metadata or {
                "autor": "Sistema Inteligente",
                "versión": "1.0",
                "fecha_creacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            log_info("Estructura del reporte construida correctamente.")
            return self.report
        except Exception as e:
            log_error(f"Error construyendo estructura del reporte: {e}")
            raise

    def add_text_sections(self, sections: dict):
        """Agrega secciones de texto descriptivas o analíticas al reporte."""
        try:
            if not isinstance(sections, dict):
                raise TypeError("sections debe ser un diccionario con {titulo: contenido}.")
            self.report["sections"].update(sections)
            log_info(f"Se agregaron {len(sections)} secciones al reporte.")
        except Exception as e:
            log_error(f"Error agregando secciones: {e}")
            raise

    def embed_charts(self, chart_paths: list):
        """Incorpora rutas de gráficos generados previamente al reporte."""
        try:
            if not isinstance(chart_paths, list):
                raise TypeError("chart_paths debe ser una lista de rutas de archivos.")
            self.report["charts"].extend(chart_paths)
            log_info(f"Se incrustaron {len(chart_paths)} gráficos en el reporte.")
        except Exception as e:
            log_error(f"Error al incrustar gráficos: {e}")
            raise

    def insert_metrics(self, model_results: dict):
        """
        Calcula e inserta métricas de rendimiento y resumen de resultados.
        model_results: Diccionario con resultados de predicción o evaluación.
        """
        try:
            if not model_results:
                log_warning("No se proporcionaron resultados del modelo; las métricas serán vacías.")
                self.report["metrics"] = {}
                self.report["sections"]["Resumen de métricas"] = "No se generaron métricas."
                return

            metrics = evaluate_model_performance(model_results)
            summary = summarize_results(metrics)
            self.report["metrics"] = metrics
            self.report["sections"]["Resumen de métricas"] = summary
            log_info("Métricas insertadas correctamente en el reporte.")
        except Exception as e:
            log_error(f"Error insertando métricas: {e}")
            raise

    def finalize_report(self, export_format="pdf", filename: str = "reporte_final"):
        """
        Genera el archivo final en el formato deseado.
        export_format: 'pdf', 'excel' o lista de ambos.
        """
        try:
            # Soporte para lista de formatos
            formats = [export_format] if isinstance(export_format, str) else export_format
            if not formats:
                raise ValueError("Debe proporcionar al menos un formato de exportación válido.")

            # Añadir timestamp automático al archivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            for fmt in formats:
                fmt_lower = fmt.lower()
                file_with_ts = f"{filename}_{timestamp}"
                if fmt_lower == "pdf":
                    export_pdf.create_pdf(self.report, f"{file_with_ts}.pdf")
                elif fmt_lower == "excel":
                    export_excel.create_excel_summary(self.report, f"{file_with_ts}.xlsx")
                else:
                    log_warning(f"Formato no soportado: {fmt}. Se ignorará.")
            log_info(f"Reporte exportado exitosamente en: {', '.join(formats).upper()}")
        except Exception as e:
            log_error(f"Error finalizando reporte: {e}")
            raise
