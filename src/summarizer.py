import os
from dataclasses import dataclass

from google import genai

from src.scraper import WikipediaArticle

GEMINI_API_KEY_VARIABLE = "GEMINI_API_KEY"
GEMINI_MODEL = "gemini-3-flash-preview"
GEMINI_TIMEOUT_SECONDS = 30
SUMMARY_PROMPT_TEMPLATE = (
    "Resume en español el siguiente artículo de Wikipedia en un solo párrafo "
    "de 3 a 5 frases. Responde únicamente con el resumen.\n\n"
    "Título: {title}\n\n{content}"
)
MISSING_API_KEY_MESSAGE = (
    f"Falta la variable de entorno {GEMINI_API_KEY_VARIABLE} con tu clave de la API de Gemini."
)
CONNECTION_ERROR_MESSAGE = "No se pudo conectar con Gemini."
INVALID_RESPONSE_MESSAGE = "Gemini no devolvió un resumen válido."
DEFAULT_HTTP_ERROR_MESSAGE = "Gemini respondió con el error {status_code}."
HTTP_ERROR_MESSAGES = {
    400: "Gemini rechazó la petición: revisa la clave y que el plan gratuito esté disponible en tu país.",
    403: "La clave de Gemini no tiene permiso para usar este modelo.",
    404: "El modelo de Gemini configurado no existe o ya no está disponible.",
    429: "Se alcanzó el límite del plan gratuito de Gemini. Inténtalo más tarde.",
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
            raise SummaryGenerationError(MISSING_API_KEY_MESSAGE)
        return api_key

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
        default_message = DEFAULT_HTTP_ERROR_MESSAGE.format(status_code=status_code)
        return HTTP_ERROR_MESSAGES.get(status_code, default_message)