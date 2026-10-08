from dataclasses import dataclass
from src.scraper import WikipediaArticle, WikipediaScraper

SUPPORTED_LANGUAGES = ("en", "fr", "de", "it", "pt")
YES_ANSWER = "s"
NO_ANSWER = "n"


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
            answer = input("¿Quieres un resumen aparte? (s/n): ").strip().lower()
            if answer in (YES_ANSWER, NO_ANSWER):
                return answer == YES_ANSWER
            print("Responde con 's' o 'n'.")