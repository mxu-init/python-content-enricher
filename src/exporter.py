from pathlib import Path

from src.summarizer import ArticleSummary

OUTPUT_DIRECTORY = Path("output")
SUMMARY_FILE_SUFFIX = "_summary.txt"
DEFAULT_SUMMARY_NAME = "article"
FILE_ENCODING = "utf-8"


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
