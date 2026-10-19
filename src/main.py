from dataclasses import dataclass
import logging
from pathlib import Path

from src.enricher import GeminiContentEnricher
from src.exporters import ExportError, PdfExporter, TxtExporter
from src.scraper import ScraperError, WikipediaArticle, WikipediaScraper
from src.summarizer import ArticleSummarizer, ArticleSummary, SummaryGenerationError
from src.translator import ContentTranslator, TranslationError

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
            
    def show_enriched_content(self, enriched_text: str) -> None:
        print("\n--- Contenido Enriquecido por IA ---\n")
        print(enriched_text)
        print()

    def show_translation(self, translated_text: str, language: str) -> None:
        print(f"\n--- Traducción ({language}) ---\n")
        print(translated_text)
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
        self._logger = logging.getLogger("content_enricher_app")
        self._cli_input = CliInput()
        self._cli_output = CliOutput()
        self._scraper = WikipediaScraper()
        self._enricher = GeminiContentEnricher(self._logger)
        self._translator = ContentTranslator(email="hernnandezfercho@gmail.com")
        self._txt_exporter = TxtExporter()
        self._pdf_exporter = PdfExporter()
        self._summarizer = ArticleSummarizer()

    def run(self) -> None:
        request = self._cli_input.ask_request()
        try:
            article = self._scraper.search(request.topic)
        except ScraperError as error:
            self._cli_output.show_error(str(error))
            return
        self._cli_output.show_article(article)

        original_text = "\n\n".join(article.paragraphs)
        enriched_text = self._enricher.enrich_content(article.title, original_text)
        self._cli_output.show_enriched_content(enriched_text)

        try:
            translated_text = self._translator.translate(enriched_text, request.language)
        except TranslationError as error:
            self._cli_output.show_error(str(error))
            return
        self._cli_output.show_translation(translated_text, request.language)

        summary = None
        if request.wants_summary:
            if not article.paragraphs:
                self._cli_output.show_error(EMPTY_SUMMARY_MESSAGE)
                return
            try:
                summary = self._summarizer.summarize(enriched_text, article.title)
            except SummaryGenerationError as error:
                self._cli_output.show_error(str(error))
                return
            self._cli_output.show_summary(summary)

        if request.wants_export:
            try:
                if request.export_format == "txt":
                    file_path = self._txt_exporter.export(request.filename, original_text, enriched_text, translated_text)
                elif request.export_format == "pdf":
                    file_path = self._pdf_exporter.export(request.filename, original_text, enriched_text, translated_text)
                print(f"¡Archivo exportado con éxito en '{file_path}'!")
            except Exception as e:
                print(f"Error al exportar: {e}")

            if summary:
                try:
                    if request.export_format == "pdf":
                        summary_file_path = self._pdf_exporter.export_summary(summary)
                    else:
                        summary_file_path = self._txt_exporter.export_summary(summary)
                    self._cli_output.show_summary_saved(summary_file_path)
                except ExportError as error:
                    self._cli_output.show_error(str(error))


if __name__ == "__main__": # pragma: no cover
    ContentEnricherApp().run()