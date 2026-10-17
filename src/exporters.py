from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from src.summarizer import ArticleSummary

OUTPUT_DIRECTORY = Path("output")
SUMMARY_FILE_SUFFIX = "_summary"
DEFAULT_SUMMARY_NAME = "article"


class ExportError(Exception):
    pass


def normalize_title(title: str) -> str:
    slug = "".join(character if character.isalnum() else "_" for character in title.lower())
    parts = [part for part in slug.split("_") if part]
    if not parts:
        return DEFAULT_SUMMARY_NAME
    return "_".join(parts)


class BaseExporter:
    def _resolve_path(self, filename: str, extension: str) -> Path:
        if not filename.endswith(f".{extension}"):
            filename = f"{filename}.{extension}"
            
        path = Path(filename)
        if not path.is_absolute() and len(path.parts) == 1:
            return OUTPUT_DIRECTORY / filename
        return path

    def _resolve_summary_path(self, summary: ArticleSummary, extension: str, filename: str | None = None) -> Path:
        if not filename:
            filename = f"{normalize_title(summary.title)}{SUMMARY_FILE_SUFFIX}.{extension}"
        return self._resolve_path(filename, extension)


class TxtExporter(BaseExporter):
    def export(self, filename: str, original: str, enriched: str, translated: str) -> Path:
        if not filename or not filename.strip():
            raise ValueError("El nombre del archivo no puede estar vacío.")
            
        path = self._resolve_path(filename, "txt")
        path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(path, "w", encoding="utf-8") as file:
                file.write("=== CONTENIDO ORIGINAL ===\n")
                file.write(f"{original}\n\n")
                
                file.write("=== CONTENIDO ENRIQUECIDO (IA) ===\n")
                file.write(f"{enriched}\n\n")
                
                file.write("=== CONTENIDO TRADUCIDO ===\n")
                file.write(f"{translated}\n")
            return path
        except OSError as e:
            raise IOError(f"Error al guardar el archivo de texto: {e}")

    def export_summary(self, summary: ArticleSummary, filename: str | None = None) -> Path:
        path = self._resolve_summary_path(summary, "txt", filename)
        try:
            self._write_file(path, summary)
        except OSError as error:
            raise ExportError(str(error)) from error
        return path

    def _write_file(self, file_path: Path, summary: ArticleSummary) -> None:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        content = f"Resumen: {summary.title}\n\n{summary.text}"
        file_path.write_text(content, encoding="utf-8")


class PdfExporter(BaseExporter):
    def export(self, filename: str, original: str, enriched: str, translated: str) -> Path:
        if not filename or not filename.strip():
            raise ValueError("El nombre del archivo no puede estar vacío.")
            
        path = self._resolve_path(filename, "pdf")
        path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            doc = SimpleDocTemplate(str(path), pagesize=letter)
            styles = getSampleStyleSheet()
            story = []

            story.append(Paragraph("Contenido Original", styles["Heading1"]))
            story.append(Paragraph(original, styles["Normal"]))
            story.append(Spacer(1, 12))

            story.append(Paragraph("Contenido Enriquecido (IA)", styles["Heading1"]))
            story.append(Paragraph(enriched, styles["Normal"]))
            story.append(Spacer(1, 12))

            story.append(Paragraph("Contenido Traducido", styles["Heading1"]))
            story.append(Paragraph(translated, styles["Normal"]))

            doc.build(story)
            return path
        except Exception as e:
            raise RuntimeError(f"Error al generar el archivo PDF: {e}")

    def export_summary(self, summary: ArticleSummary, filename: str | None = None) -> Path:
        path = self._resolve_summary_path(summary, "pdf", filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            doc = SimpleDocTemplate(str(path), pagesize=letter)
            styles = getSampleStyleSheet()
            story = [
                Paragraph(f"Resumen: {summary.title}", styles["Heading1"]),
                Spacer(1, 12),
                Paragraph(summary.text, styles["Normal"]),
            ]
            doc.build(story)
        except Exception as error:
            raise ExportError(str(error)) from error
        return path