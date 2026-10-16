import re

import requests
from deep_translator import GoogleTranslator
from deep_translator.exceptions import BaseError

SOURCE_LANGUAGE = "es"
PARAGRAPH_SEPARATOR = "\n\n"
SENTENCE_BOUNDARY = re.compile(r"(?<=[.!?])\s+")
MAX_CHUNK_LENGTH = 1500
TRANSLATION_ERROR_MESSAGE = "No se pudo traducir el contenido. Inténtalo de nuevo más tarde."


class TranslationError(Exception):
    pass


class ContentTranslator:
    def translate(self, text: str, target_language: str) -> str:
        paragraphs = [
            paragraph
            for paragraph in text.split(PARAGRAPH_SEPARATOR)
            if paragraph.strip()
        ]
        try:
            translator = GoogleTranslator(
                source=SOURCE_LANGUAGE, target=target_language
            )
            translated_paragraphs = [
                self._translate_paragraph(translator, paragraph)
                for paragraph in paragraphs
            ]
        except (BaseError, requests.exceptions.RequestException) as error:
            raise TranslationError(TRANSLATION_ERROR_MESSAGE) from error
        return PARAGRAPH_SEPARATOR.join(translated_paragraphs)

    def _translate_paragraph(self, translator: GoogleTranslator, paragraph: str) -> str:
        chunks = self._split_into_chunks(paragraph)
        return " ".join(translator.translate(chunk) for chunk in chunks)

    def _split_into_chunks(self, paragraph: str) -> list[str]:
        chunks = []
        current_chunk = ""
        for sentence in SENTENCE_BOUNDARY.split(paragraph):
            if current_chunk and len(current_chunk) + len(sentence) + 1 > MAX_CHUNK_LENGTH:
                chunks.append(current_chunk)
                current_chunk = sentence
            else:
                current_chunk = f"{current_chunk} {sentence}".strip()
        chunks.append(current_chunk)
        return chunks
