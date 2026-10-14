import logging
import os
import socket
import ssl
import time
from typing import Optional

_original_getaddrinfo = socket.getaddrinfo


def _ipv4_only_getaddrinfo(*args, **kwargs):
    results = _original_getaddrinfo(*args, **kwargs)
    return [res for res in results if res[0] == socket.AF_INET]


socket.getaddrinfo = _ipv4_only_getaddrinfo

import httpx
from dotenv import load_dotenv
from google import genai
from google.genai import types

GEMINI_MODEL = "gemini-3.8-flash"
HTTP_CONNECT_TIMEOUT = 10.0
HTTP_READ_TIMEOUT = 90.0
MAX_RETRIES = 3
RETRY_BASE_DELAY_SECONDS = 2
ENRICHMENT_FALLBACK = "[Enriquecimiento no disponible: error al contactar con la IA.]"
MISSING_KEY_FALLBACK = "[Enriquecimiento no disponible: falta la clave GEMINI_API_KEY.]"

_RETRYABLE_ERRORS = (ssl.SSLError, TimeoutError, ConnectionError, OSError, httpx.TimeoutException)


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
        http_client = httpx.Client(
            timeout=httpx.Timeout(
                HTTP_READ_TIMEOUT,
                connect=HTTP_CONNECT_TIMEOUT,
            ),
        )
        return genai.Client(
            api_key=self._api_key,
            http_options=types.HttpOptions(
                httpx_client=http_client,
                retry_options=types.HttpRetryOptions(
                    attempts=MAX_RETRIES,
                    initial_delay=RETRY_BASE_DELAY_SECONDS,
                    max_delay=30.0,
                ),
            ),
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
        last_error: Optional[Exception] = None

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                self.logger.info(
                    "Enviando solicitud de enriquecimiento a Gemini (intento %d/%d).",
                    attempt,
                    MAX_RETRIES,
                )
                response = self._client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=prompt,
                    config=types.GenerateContentConfig(temperature=0.7),
                )
                self.logger.info("Respuesta de Gemini recibida correctamente.")
                return response.text
            except _RETRYABLE_ERRORS as error:
                last_error = error
                delay = RETRY_BASE_DELAY_SECONDS ** attempt
                self.logger.warning(
                    "Error de red/SSL en intento %d/%d: %s — %s. Reintentando en %ds...",
                    attempt,
                    MAX_RETRIES,
                    type(error).__name__,
                    error,
                    delay,
                )
                if attempt < MAX_RETRIES:
                    time.sleep(delay)
            except Exception as error:
                last_error = error
                self.logger.error(
                    "Error no recuperable al contactar con Gemini (%s): %s",
                    type(error).__name__,
                    error,
                )
                break

        self.logger.error(
            "Fallo definitivo tras %d intento(s). Ultimo error (%s): %s. "
            "Verifica conectividad a generativelanguage.googleapis.com "
            "(posible bloqueo de firewall/VPN).",
            MAX_RETRIES,
            type(last_error).__name__,
            last_error,
        )
        return ENRICHMENT_FALLBACK
