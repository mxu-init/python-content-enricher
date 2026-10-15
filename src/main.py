from dataclasses import dataclass
from pathlib import Path

from src.exporter import ExportError, SummaryTextExporter
from src.scraper import ScraperError, WikipediaArticle, WikipediaScraper
from src.exporters import TxtExporter, PdfExporter
from src.summarizer import ArticleSummarizer, ArticleSummary, SummaryGenerationError

SUPPORTED_LANGUAGES = ("en", "fr", "de", "it", "pt")
YES_ANSWER = "s"
NO_ANSWER = "n"
EMPTY_SUMMARY_MESSAGE = "No hay contenido suficiente para generar el resumen."


@dataclass
class UserRequest:
    topic: str
    language: str
    wants_summary: bool
    wants_export: bool
    filename: str
    export_format: str


class CliInput:
    def ask_request(self) -> UserRequest:
        topic = self._ask_topic()
        language = self._ask_language()
        wants_summary = self._ask_summary()
        wants_export, filename, export_format = self._ask_export()
        
        return UserRequest(
            topic, language, wants_summary, wants_export, filename, export_format
        )

    def _ask_topic(self) -> str:
        while True:
            topic = input("Tema a investigar: ").strip()
            if topic:
                return topic
            print("El tema no puede estar vacío.")

    def _ask_language(self) -> str:
        options = ", ".join(SUPPORTED_LANGUAGES)
        while True:
            language = input(f"Idioma de traducción ({options}): ").strip().lower()
            if language in SUPPORTED_LANGUAGES:
                return language
            print(f"Idioma no válido. Opciones: {options}.")

    def _ask_summary(self) -> bool:
        while True:
            answer = input("¿Quieres ver el resumen del tema? (s/n): ").strip().lower()
            if answer in (YES_ANSWER, NO_ANSWER):
                return answer == YES_ANSWER
            print("Responde con 's' o 'n'.")

    def ask_export(self) -> bool:
        while True:
            answer = input("¿Quieres guardar el resumen en un archivo? (s/n): ").strip().lower()
            if answer in (YES_ANSWER, NO_ANSWER):
                return answer == YES_ANSWER
            print("Responde con 's' o 'n'.")

    def _ask_export(self) -> tuple[bool, str, str]:
        while True:
            answer = input("¿Quieres exportar el resultado a un archivo? (s/n): ").strip().lower()
            if answer == NO_ANSWER:
                return False, "", ""
            if answer == YES_ANSWER:
                break
            print("Responde con 's' o 'n'.")

        while True:
            filename = input("Nombre del archivo: ").strip()
            if filename:
                break
            print("El nombre del archivo no puede estar vacío.")

        while True:
            fmt = input("Formato de exportación (txt/pdf): ").strip().lower()
            if fmt in ("txt", "pdf"):
                return True, filename, fmt
            print("Formato no válido. Debe ser 'txt' o 'pdf'.")


class CliOutput:
    def show_article(self, article: WikipediaArticle) -> None:
        print(f"\n{article.title}\n")
        for paragraph in article.paragraphs:
            print(paragraph)
            print()
    
    def show_error(self, message: str) -> None:
        print(f"[Error]: {message}")

    def show_summary(self, summary: ArticleSummary) -> None:
        print(f"\nResumen: {summary.title}\n")
        print(summary.text)

    def show_summary_saved(self, file_path: Path) -> None:
        print(f"Resumen guardado en: {file_path}")


class ContentEnricherApp:
    def __init__(self) -> None:
        self._cli_input = CliInput()
        self._cli_output = CliOutput()
        self._scraper = WikipediaScraper()
        self._txt_exporter = TxtExporter()
        self._pdf_exporter = PdfExporter()
        self._summarizer = ArticleSummarizer()
        self._summary_exporter = SummaryTextExporter()

    def run(self) -> None:
        request = self._cli_input.ask_request()
        try:
            article = self._scraper.search(request.topic)
        except ScraperError as error:
            self._cli_output.show_error(str(error))
            return
        self._cli_output.show_article(article)

        if request.wants_export:
            # Unimos los párrafos del artículo simulando el contenido original 
            # (y puedes adaptar las variables de enriquecido/traducido según los siguientes módulos)
            content_text = "\n\n".join(article.paragraphs)
            
            try:
                if request.export_format == "txt":
                    self._txt_exporter.export(request.filename, content_text, "[Contenido enriquecido pendiente]", "[Contenido traducido pendiente]")
                elif request.export_format == "pdf":
                    self._pdf_exporter.export(request.filename, content_text, "[Contenido enriquecido pendiente]", "[Contenido traducido pendiente]")
                print(f"¡Archivo exportado con éxito como '{request.filename}'!")
            except Exception as e:
                print(f"Error al exportar: {e}")


if __name__ == "__main__": # pragma: no cover
    ContentEnricherApp().run()