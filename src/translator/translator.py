from deep_translator import GoogleTranslator

class DeepTranslatorService:
    """Clase para realizar traducciones automáticas del contenido utilizando la API de Deep Translate."""

    def __init__(self, logger):
        self.logger = logger

    def translate(self, text: str, target_language: str) -> str:
        """Traduce el texto completo al idioma objetivo (ej. 'en', 'fr', 'de', 'it', 'es')."""
        self.logger.info(f"Iniciando traducción al idioma '{target_language}'...")
        try:
            # Dividir texto en bloques para evitar superar límites de caracteres de API
            chunks = [text[i:i+4500] for i in range(0, len(text), 4500)]
            translated_chunks = []

            translator = GoogleTranslator(source='auto', target=target_language)
            for chunk in chunks:
                translated_chunks.append(translator.translate(chunk))

            translated_text = "\n".join(translated_chunks)
            self.logger.info("Traducción completada con éxito.")
            return translated_text
        except Exception as e:
            self.logger.error(f"Error durante la traducción: {e}")
            raise RuntimeError(f"Error al traducir el contenido al idioma '{target_language}': {e}")