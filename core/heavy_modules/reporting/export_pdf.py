# core/heavy_modules/reporting/export_pdf.py

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from core.utils.logger import log_info, log_error


def add_images(story: list, charts: list):
    """
    Inserta gráficos en el PDF a partir de rutas de imagen.
    """
    for chart_path in charts:
        try:
            story.append(Image(chart_path, width=400, height=250))
            story.append(Spacer(1, 10))
        except Exception:
            log_error(f"No se pudo insertar gráfico: {chart_path}")


def add_table(story: list, metrics: dict):
    """
    Inserta una tabla con métricas en el PDF.
    """
    if not metrics:
        return

    data = [["Métrica", "Valor"]] + [[k, f"{v:.4f}"] for k, v in metrics.items()]
    table = Table(data, hAlign='LEFT')
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black)
    ]))
    story.append(table)
    story.append(Spacer(1, 12))


def save_pdf(doc: SimpleDocTemplate, story: list, filename: str):
    """
    Construye y guarda el PDF en disco.
    """
    try:
        doc.build(story)
        log_info(f"PDF generado correctamente: {filename}")
    except Exception as e:
        log_error(f"Error guardando PDF: {e}")
        raise


def create_pdf(report_data: dict, filename: str):
    """
    Crea un PDF completo a partir de report_data, incluyendo título, secciones,
    imágenes, métricas y metadatos.
    """
    try:
        doc = SimpleDocTemplate(filename, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []

        # Título principal
        story.append(Paragraph(report_data.get("title", "Reporte"), styles["Title"]))
        story.append(Spacer(1, 12))

        # Metadatos
        metadata = report_data.get("metadata", {})
        for key, value in metadata.items():
            story.append(Paragraph(f"<b>{key.capitalize()}:</b> {value}", styles["Normal"]))
        story.append(Spacer(1, 12))

        # Secciones de texto
        for section_title, content in report_data.get("sections", {}).items():
            story.append(Paragraph(f"<b>{section_title}</b>", styles["Heading2"]))
            story.append(Paragraph(content, styles["Normal"]))
            story.append(Spacer(1, 10))

        # Gráficos
        add_images(story, report_data.get("charts", []))

        # Métricas
        add_table(story, report_data.get("metrics", {}))

        # Guardar PDF
        save_pdf(doc, story, filename)

    except Exception as e:
        log_error(f"Error generando PDF: {e}")
        raise
