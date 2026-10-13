import re
from pathlib import Path

from src.summarizer import ArticleSummary

OUTPUT_DIRECTORY = Path(__file__).resolve().parent.parent / "output"
SUMMARY_FILE_SUFFIX = "_summary.txt"
DEFAULT_FILE_STEM = "article"
FILE_ENCODING = "utf-8"
UNSAFE_FILE_NAME_CHARACTERS = re.compile(r"[^\w\-]+")


class ExportError(Exception):
    pass


class SummaryTextExporter:
    def __init__(self, output_directory: Path = OUTPUT_DIRECTORY) -> None:
        self._output_directory = output_directory

    def export(self, summary: ArticleSummary) -> Path:
        file_path = self._output_directory / self._build_file_name(summary.title)
        try:
            self._output_directory.mkdir(parents=True, exist_ok=True)
            file_path.write_text(self._format_content(summary), encoding=FILE_ENCODING)
        except OSError as error:
            raise ExportError(f"No se pudo guardar el resumen en {file_path}.") from error
        return file_path

    def _build_file_name(self, title: str) -> str:
        file_stem = UNSAFE_FILE_NAME_CHARACTERS.sub("_", title.strip().lower()).strip("_")
        return f"{file_stem or DEFAULT_FILE_STEM}{SUMMARY_FILE_SUFFIX}"

    def _format_content(self, summary: ArticleSummary) -> str:
        return f"Resumen: {summary.title}\n\n{summary.text}\n"