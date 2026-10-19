from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.platypus.doctemplate import LayoutError

from src.summarizer import ArticleSummary

OUTPUT_DIRECTORY = Path("output")
SUMMARY_FILE_SUFFIX = "_summary.txt"
DEFAULT_SUMMARY_NAME = "article"
FILE_ENCODING = "utf-8"
EXPORT_FORMATS = ("txt", "md", "pdf")
SUMMARY_KIND = "summary"
TOPIC_KIND = "topic"
CONTENT_HEADINGS = {SUMMARY_KIND: "Resumen", TOPIC_KIND: "Tema investigado"}
EXPORT_DATE_FORMAT = "%Y-%m-%d"
PDF_SPACER_HEIGHT = 12
UNSUPPORTED_FORMAT_MESSAGE = "Formato de exportación no válido: '{export_format}'. Opciones: {options}."
PERMISSION_ERROR_MESSAGE = "No hay permisos para escribir en '{directory}'."
INVALID_PATH_MESSAGE = "La ruta de destino '{path}' no es válida."
GENERIC_WRITE_ERROR_MESSAGE = "No se pudo guardar el archivo '{path}': {detail}"
PDF_LAYOUT_ERROR_MESSAGE = "No se pudo generar el PDF: el contenido no cabe en la página."


class ExportError(Exception):
    pass


class SummaryTextExporter:
    def export(self, summary: ArticleSummary) -> Path:
        file_path = self._build_file_path(summary)
        try:
            self._write_file(file_path, summary)
        except OSError as error:
            raise ExportError(str(error)) from error
        return file_path

    def _build_file_path(self, summary: ArticleSummary) -> Path:
        filename = f"{self._normalize_title(summary.title)}{SUMMARY_FILE_SUFFIX}"
        return OUTPUT_DIRECTORY / filename

    def _normalize_title(self, title: str) -> str:
        slug = "".join(character if character.isalnum() else "_" for character in title.lower())
        parts = [part for part in slug.split("_") if part]
        if not parts:
            return DEFAULT_SUMMARY_NAME
        return "_".join(parts)

    def _write_file(self, file_path: Path, summary: ArticleSummary) -> None:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        content = f"Resumen: {summary.title}\n\n{summary.text}"
        file_path.write_text(content, encoding=FILE_ENCODING)


class ContentExporter(SummaryTextExporter):
    def export_content(
        self, title: str, text: str, export_format: str, content_kind: str
    ) -> Path:
        if export_format not in EXPORT_FORMATS:
            raise ExportError(
                UNSUPPORTED_FORMAT_MESSAGE.format(
                    export_format=export_format, options=", ".join(EXPORT_FORMATS)
                )
            )
        file_path = self._build_content_path(title, content_kind, export_format)
        heading = f"{CONTENT_HEADINGS[content_kind]}: {title}"
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            self._write_content(file_path, heading, text, export_format)
        except OSError as error:
            raise ExportError(self._describe_write_error(error, file_path)) from error
        except LayoutError as error:
            raise ExportError(PDF_LAYOUT_ERROR_MESSAGE) from error
        return file_path

    def _build_content_path(self, title: str, content_kind: str, export_format: str) -> Path:
        today = date.today().strftime(EXPORT_DATE_FORMAT)
        topic = self._normalize_title(title)
        return OUTPUT_DIRECTORY / f"{today}_{topic}_{content_kind}.{export_format}"

    def _write_content(
        self, file_path: Path, heading: str, text: str, export_format: str
    ) -> None:
        if export_format == "pdf":
            self._write_pdf(file_path, heading, text)
            return
        title_line = f"# {heading}" if export_format == "md" else heading
        file_path.write_text(f"{title_line}\n\n{text}\n", encoding=FILE_ENCODING)

    def _write_pdf(self, file_path: Path, heading: str, text: str) -> None:
        styles = getSampleStyleSheet()
        story = [Paragraph(escape(heading), styles["Heading1"])]
        for block in text.split("\n\n"):
            story.append(Paragraph(escape(block), styles["Normal"]))
            story.append(Spacer(1, PDF_SPACER_HEIGHT))
        SimpleDocTemplate(str(file_path), pagesize=letter).build(story)

    def _describe_write_error(self, error: OSError, file_path: Path) -> str:
        if isinstance(error, PermissionError):
            return PERMISSION_ERROR_MESSAGE.format(directory=file_path.parent)
        if isinstance(error, (FileNotFoundError, NotADirectoryError, IsADirectoryError)):
            return INVALID_PATH_MESSAGE.format(path=file_path)
        if isinstance(error, FileExistsError):
            return INVALID_PATH_MESSAGE.format(path=file_path.parent)
        return GENERIC_WRITE_ERROR_MESSAGE.format(
            path=file_path, detail=error.strerror or error
        )