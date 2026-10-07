import os
from google import genai

class AIEnricher:
    """Clase encargada de enriquecer el texto y generar resúmenes mediante Google Gemini API."""

    def __init__(self, logger, api_key: str = None):
        self.logger = logger
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            self.logger.warning("GEMINI_API_KEY no configurada. Se usará el modo de respaldo.")
            self.client = None
        else:
            self.client = genai.Client(api_key=self.api_key)

    def enrich_content(self, title: str, text: str) -> str:
        """Enriquece el texto agregando contexto, explicaciones clave y datos relevantes."""
        self.logger.info("Enriqueciendo contenido con IA (Gemini)...")
        if not self.client:
            return f"[ENRIQUECIMIENTO MOCK - Sin API Key]\n\n{text}\n\n*Contexto Adicional:* Este tema ({title}) abarca conceptos fundamentales en su área de conocimiento."

        prompt = (
            f"Eres un experto en investigación académica. Enriquece el siguiente texto sobre '{title}'. "
            "Añade ejemplos prácticos, amplía los conceptos complejos y dale una estructura muy clara de estudio.\n\n"
            f"Texto original:\n{text}"
        )

        try:
            response = self.client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt,
            )
            enriched_text = response.text
            self.logger.info("Contenido enriquecido exitosamente por IA.")
            return enriched_text
        except Exception as e:
            self.logger.error(f"Error durante el enriquecimiento con Gemini: {e}")
            raise RuntimeError("Fallo en la comunicación con el servicio de IA.")

    def generate_summary(self, text: str) -> str:
        """Genera un resumen ejecutivo en puntos clave (bullet points) a partir del texto enriquecido."""
        self.logger.info("Generando resumen del contenido enriquecido...")
        if not self.client:
            return "• Resumen de ejemplo: Conceptos clave analizados correctamente."

        prompt = (
            "Sintetiza el siguiente texto en un resumen ejecutivo corto con viñetas (bullet points) "
            "resaltando las ideas principales para estudio rápido:\n\n" + text
        )

        try:
            response = self.client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt,
            )
            summary = response.text
            self.logger.info("Resumen generado exitosamente.")
            return summary
        except Exception as e:
            self.logger.error(f"Error al generar resumen: {e}")
            return "No se pudo generar el resumen debido a un error técnico."