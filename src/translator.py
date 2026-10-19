import os
import re

import requests
from deep_translator import MyMemoryTranslator
from deep_translator.exceptions import BaseError, TooManyRequests

SOURCE_LANGUAGE = "es-ES"
TARGET_LANGUAGE_MAPPING = {
    "en": "en-GB",
    "fr": "fr-FR",
    "de": "de-DE",
    "it": "it-IT",
    "pt": "pt-PT",
}
PARAGRAPH_SEPARATOR = "\n\n"
SENTENCE_BOUNDARY = re.compile(r"(?<=[.!?])\s+")
MAX_CHUNK_LENGTH = 400
TRANSLATION_ERROR_MESSAGE = "No se pudo traducir el contenido. Inténtalo de nuevo más tarde."
DAILY_LIMIT_MESSAGE = "Se ha alcanzado el límite de traducción de MyMemory. Inténtalo más tarde o añade MYMEMORY_EMAIL."
MYMEMORY_WARNING = "MYMEMORY WARNING"


class TranslationError(Exception):
    pass


class ContentTranslator:
    def __init__(self, email: str | None = None) -> None:
        self._email = email or os.getenv("MYMEMORY_EMAIL")

    def translate(self, text: str, target_language: str) -> str:
        paragraphs = [
            paragraph
            for paragraph in text.split(PARAGRAPH_SEPARATOR)
            if paragraph.strip()
        ]
        resolved_language = TARGET_LANGUAGE_MAPPING.get(
            target_language, target_language
        )
        try:
            translator = MyMemoryTranslator(
                source=SOURCE_LANGUAGE,
                target=resolved_language,
                email=self._email,
            )
            translated_paragraphs = [
                self._translate_paragraph(translator, paragraph)
                for paragraph in paragraphs
            ]
        except (BaseError, TooManyRequests, requests.exceptions.RequestException) as error:
            raise TranslationError(TRANSLATION_ERROR_MESSAGE) from error
        return PARAGRAPH_SEPARATOR.join(translated_paragraphs)

    def _translate_paragraph(self, translator: MyMemoryTranslator, paragraph: str) -> str:
        chunks = self._split_into_chunks(paragraph)
        return " ".join(self._translate_chunk(translator, chunk) for chunk in chunks)

    def _translate_chunk(self, translator: MyMemoryTranslator, chunk: str) -> str:
        result = translator.translate(chunk)
        if result and MYMEMORY_WARNING in result:
            raise TranslationError(DAILY_LIMIT_MESSAGE)
        return result

    def _split_into_chunks(self, paragraph: str) -> list[str]:
        chunks = []
        current_chunk = ""
        for sentence in SENTENCE_BOUNDARY.split(paragraph):
            sub_sentences = self._split_long_sentence(sentence)
            for sub_sentence in sub_sentences:
                if current_chunk and len(current_chunk) + len(sub_sentence) + 1 > MAX_CHUNK_LENGTH:
                    chunks.append(current_chunk)
                    current_chunk = sub_sentence
                else:
                    current_chunk = f"{current_chunk} {sub_sentence}".strip()
        if current_chunk:
            chunks.append(current_chunk)
        return chunks

    def _split_long_sentence(self, sentence: str) -> list[str]:
        if len(sentence) <= MAX_CHUNK_LENGTH:
            return [sentence]
        words = sentence.split(" ")
        sub_chunks = []
        current = ""
        for word in words:
            if current and len(current) + len(word) + 1 > MAX_CHUNK_LENGTH:
                sub_chunks.append(current)
                current = word
            else:
                current = f"{current} {word}".strip()
        if current:
            sub_chunks.append(current)
        return sub_chunks
