from abc import ABC, abstractmethod
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

class DocumentExporterStrategy(ABC):
    """Interfaz abstracta para la estrategia de exportación de archivos."""
    @abstractmethod
    def export(self, filename: str, title: str, original: str, enriched: str, summary: str, translated: str) -> str:
        pass

class TextExporter(DocumentExporterStrategy):
    """Exportador a formato plano .txt."""

    def __init__(self, logger):
        self.logger = logger

    def export(self, filename: str, title: str, original: str, enriched: str, summary: str, translated: str) -> str:
        output_path = Path(f"output/{filename}.txt")
        output_path.parent.mkdir(exist_ok=True)

        content = (
            f"==================================================\n"
            f" INFORME DE ENRIQUECIMIENTO: {title.upper()}\n"
            f"==================================================\n\n"
            f"--- 1. CONTENIDO ORIGINAL (WIKIPEDIA) ---\n{original}\n\n"
            f"--- 2. CONTENIDO ENRIQUECIDO CON IA ---\n{enriched}\n\n"
            f"--- 3. RESUMEN EJECUTIVO ---\n{summary}\n\n"
            f"--- 4. TRADUCCIÓN DE CONTENIDO ---\n{translated}\n"
        )

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        self.logger.info(f"Archivo TXT exportado exitosamente en: {output_path.resolve()}")
        return str(output_path.resolve())

class PdfExporter(DocumentExporterStrategy):
    """Exportador a formato PDF profesional usando ReportLab."""

    def __init__(self, logger):
        self.logger = logger

    def export(self, filename: str, title: str, original: str, enriched: str, summary: str, translated: str) -> str:
        output_path = Path(f"output/{filename}.pdf")
        output_path.parent.mkdir(exist_ok=True)

        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=letter,
            rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
        )

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontSize=20, textColor=colors.HexColor("#1A365D"), spaceAfter=15)
        section_style = ParagraphStyle('DocSection', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor("#2B6CB0"), spaceBefore=12, spaceAfter=8)
        body_style = ParagraphStyle('DocBody', parent=styles['BodyText'], fontSize=10, leading=14, spaceAfter=8)

        story = []
        story.append(Paragraph(f"Informe de Estudio: {title}", title_style))
        story.append(Spacer(1, 10))

        sections = [
            ("1. Contenido Original de Wikipedia", original),
            ("2. Contenido Enriquecido por IA", enriched),
            ("3. Resumen Ejecutivo", summary),
            ("4. Contenido Traducido", translated),
        ]

        for sec_title, sec_text in sections:
            story.append(Paragraph(sec_title, section_style))
            # Reemplazar saltos de línea con etiquetas de párrafo para ReportLab
            for para in sec_text.split("\n\n"):
                if para.strip():
                    story.append(Paragraph(para.strip().replace("\n", "<br/>"), body_style))
            story.append(Spacer(1, 10))

        doc.build(story)
        self.logger.info(f"Archivo PDF exportado exitosamente en: {output_path.resolve()}")
        return str(output_path.resolve())