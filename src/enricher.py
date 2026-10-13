import logging
import os
from typing import Optional

from dotenv import load_dotenv
from google import genai
from google.genai import types

GEMINI_MODEL = "gemini-2.5-flash"
REQUEST_TIMEOUT_SECONDS = 30
ENRICHMENT_FALLBACK = "[Enriquecimiento no disponible: error al contactar con la IA.]"
MISSING_KEY_FALLBACK = "[Enriquecimiento no disponible: falta la clave GEMINI_API_KEY.]"


def setup_logger() -> logging.Logger:
    logger = logging.getLogger("enricher")
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


class GeminiContentEnricher:
    """Enriches article content using Google Gemini via the google-genai SDK."""

    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        self.logger = logger or setup_logger()
        load_dotenv()
        self._api_key = os.getenv("GEMINI_API_KEY")
        self._client = self._build_client()

    def _build_client(self) -> Optional[genai.Client]:
        if not self._api_key:
            self.logger.warning("GEMINI_API_KEY no encontrada. El enriquecimiento estara desactivado.")
            return None
        return genai.Client(
            api_key=self._api_key,
            http_options=types.HttpOptions(timeout=REQUEST_TIMEOUT_SECONDS),
        )

    def enrich_content(self, title: str, original_text: str) -> str:
        if self._client is None:
            self.logger.error("Cliente Gemini no inicializado. Devolviendo fallback.")
            return MISSING_KEY_FALLBACK

        prompt = self._build_prompt(title, original_text)
        return self._request_enrichment(prompt)

    def _build_prompt(self, title: str, original_text: str) -> str:
        return (
            f"Eres un asistente educativo experto. A continuacion encontraras un articulo sobre '{title}'.\n\n"
            f"TEXTO ORIGINAL:\n{original_text}\n\n"
            "Tu tarea es enriquecer este articulo de forma estructurada:\n"
            "1. **Contexto y relevancia**: Explica por que este tema es importante.\n"
            "2. **Conceptos clave**: Define y amplia los conceptos mas complejos del texto.\n"
            "3. **Notas de estudio**: Proporciona 3-5 puntos clave para recordar.\n"
            "4. **Conclusion**: Resume el aprendizaje principal en 2-3 frases.\n\n"
            "Responde en espanol y de forma clara, directa y educativa."
        )

    def _request_enrichment(self, prompt: str) -> str:
        try:
            self.logger.info("Enviando solicitud de enriquecimiento a Gemini.")
            response = self._client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
            )
            self.logger.info("Respuesta de Gemini recibida correctamente.")
            return response.text
        except Exception as error:
            self.logger.error("Error al contactar con Gemini: %s", error)
            return ENRICHMENT_FALLBACK
