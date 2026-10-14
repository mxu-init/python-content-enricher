from dataclasses import dataclass

from src.scraper import WikipediaArticle, WikipediaScraper
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


class CliInput:
    def ask_request(self) -> UserRequest:
        return UserRequest(
            topic=self._ask_topic(),
            language=self._ask_language(),
            wants_summary=self._ask_summary(),
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

class CliOutput:
    def show_article(self, article: WikipediaArticle) -> None:
        print(f"\n{article.title}\n")
        for paragraph in article.paragraphs:
            print(paragraph)
            print()

    def show_summary(self, summary: ArticleSummary) -> None:
        print(f"\nResumen: {summary.title}\n")
        print(summary.text)

    def show_error(self, message: str) -> None:
        print(message)


class ContentEnricherApp:
    def __init__(self) -> None:
        self._cli_input = CliInput()
        self._cli_output = CliOutput()
        self._scraper = WikipediaScraper()
        self._summarizer = ArticleSummarizer()

    def run(self) -> None:
        request = self._cli_input.ask_request()
        article = self._scraper.search(request.topic)
        self._cli_output.show_article(article)
        if request.wants_summary:
            self._generate_summary(article)

    def _generate_summary(self, article: WikipediaArticle) -> None:
        if not article.paragraphs:
            self._cli_output.show_error(EMPTY_SUMMARY_MESSAGE)
            return
        try:
            summary = self._summarizer.summarize(article)
        except SummaryGenerationError as error:
            self._cli_output.show_error(str(error))
            return
        self._cli_output.show_summary(summary)


if __name__ == "__main__": # pragma: no cover
    ContentEnricherApp().run()