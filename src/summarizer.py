import os
from dataclasses import dataclass
from pathlib import Path

from google import genai

from src.scraper import WikipediaArticle

GEMINI_API_KEY_VARIABLE = "GEMINI_API_KEY"
GEMINI_MODEL = "gemini-3-flash-preview"
GEMINI_TIMEOUT_SECONDS = 30
ENV_FILE_NAME = ".env"
ENV_FILE_DIRECTORY = Path(__file__).resolve().parent.parent
SUMMARY_PROMPT_TEMPLATE = (
    "Resume en español el siguiente artículo de Wikipedia en exactamente tres "
    "párrafos separados por una línea en blanco, cada uno de dos a tres frases. "
    "No uses viñetas ni títulos. Responde únicamente con los tres párrafos.\n\n"
    "Título: {title}\n\n{content}"
)
MISSING_API_KEY_MESSAGE = (
    "No se pudo generar el resumen: falta la clave de API de Gemini. "
    "Por favor, inténtelo más tarde."
)
CONNECTION_ERROR_MESSAGE = "No se pudo conectar con Gemini. Por favor, inténtelo más tarde."
INVALID_RESPONSE_MESSAGE = (
    "Gemini no devolvió un resumen válido. Por favor, inténtelo más tarde."
)
DEFAULT_HTTP_ERROR_MESSAGE = "Gemini no respondió correctamente. Por favor, inténtelo más tarde."
HTTP_ERROR_MESSAGES = {
    400: "La clave de API de Gemini no es válida. Por favor, inténtelo más tarde.",
    403: "La clave de API de Gemini no tiene permiso para usar este modelo. Por favor, inténtelo más tarde.",
    404: "El modelo de Gemini solicitado no está disponible. Por favor, inténtelo más tarde.",
    429: "Se alcanzó el límite de solicitudes de Gemini. Por favor, inténtelo más tarde.",
}


class SummaryGenerationError(Exception):
    pass


@dataclass
class ArticleSummary:
    title: str
    text: str


class ArticleSummarizer:
    def summarize(self, article: WikipediaArticle) -> ArticleSummary:
        api_key = self._read_api_key()
        prompt = self._build_prompt(article)
        text = self._request_summary(api_key, prompt)
        if not text:
            raise SummaryGenerationError(INVALID_RESPONSE_MESSAGE)
        return ArticleSummary(title=article.title, text=text)

    def _read_api_key(self) -> str:
        api_key = os.environ.get(GEMINI_API_KEY_VARIABLE, "").strip()
        if not api_key:
            api_key = self._read_api_key_from_env_file()
        if not api_key:
            raise SummaryGenerationError(MISSING_API_KEY_MESSAGE)
        return api_key

    def _read_api_key_from_env_file(self) -> str:
        env_file = ENV_FILE_DIRECTORY / ENV_FILE_NAME
        if not env_file.is_file():
            return ""
        for line in env_file.read_text(encoding="utf-8").splitlines():
            name, separator, value = line.partition("=")
            if separator and name.strip() == GEMINI_API_KEY_VARIABLE:
                return value.strip().strip('"').strip("'")
        return ""

    def _build_prompt(self, article: WikipediaArticle) -> str:
        return SUMMARY_PROMPT_TEMPLATE.format(
            title=article.title, content="\n\n".join(article.paragraphs)
        )

    def _request_summary(self, api_key: str, prompt: str) -> str:
        client = genai.Client(api_key=api_key)
        try:
            interaction = client.interactions.create(
                model=GEMINI_MODEL,
                input=prompt,
                timeout=GEMINI_TIMEOUT_SECONDS,
            )
        except Exception as error:
            raise SummaryGenerationError(self._describe_error(error)) from error
        return (interaction.output_text or "").strip()

    def _describe_error(self, error: Exception) -> str:
        status_code = getattr(error, "status_code", None)
        if status_code is None:
            return CONNECTION_ERROR_MESSAGE
        return HTTP_ERROR_MESSAGES.get(status_code, DEFAULT_HTTP_ERROR_MESSAGE)