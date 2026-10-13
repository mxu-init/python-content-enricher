from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup

WIKIPEDIA_SEARCH_URL = "https://es.wikipedia.org/w/index.php"
SEARCH_RESULTS_URL_MARKER = "search="
REQUEST_HEADERS = {"User-Agent": "ContentEnricher/1.0 (course project)"}
REQUEST_TIMEOUT_SECONDS = 10
PARAGRAPH_LIMIT = 5


class ScraperError(Exception):
    pass


class TopicNotFoundError(ScraperError):
    pass


class WikipediaConnectionError(ScraperError):
    pass


class WikipediaTimeoutError(ScraperError):
    pass


class EmptyArticleError(ScraperError):
    pass


@dataclass
class WikipediaArticle:
    title: str
    paragraphs: list[str]


class ArticleParser:
    def parse(self, html: str) -> WikipediaArticle:
        soup = BeautifulSoup(html, "html.parser")
        return WikipediaArticle(
            title=self._extract_title(soup),
            paragraphs=self._extract_paragraphs(soup),
        )

    def _extract_title(self, soup: BeautifulSoup) -> str:
        return soup.find(id="firstHeading").get_text(strip=True)

    def _extract_paragraphs(self, soup: BeautifulSoup) -> list[str]:
        paragraph_tags = soup.select("#mw-content-text .mw-parser-output p")
        texts = [self._clean_paragraph(tag) for tag in paragraph_tags]
        non_empty_texts = [text for text in texts if text]
        return non_empty_texts[:PARAGRAPH_LIMIT]

    def _clean_paragraph(self, paragraph_tag) -> str:
        for citation in paragraph_tag.select("sup"):
            citation.decompose()
        return " ".join(paragraph_tag.get_text().split())


class WikipediaScraper:
    def __init__(self) -> None:
        self._parser = ArticleParser()

    def search(self, topic: str) -> WikipediaArticle:
        html = self._fetch_html(topic)
        article = self._parser.parse(html)
        if not article.paragraphs:
            raise EmptyArticleError(
                f"El artículo '{topic}' no contiene suficiente información."
            )
        return article

    def _fetch_html(self, topic: str) -> str:
        try:
            response = requests.get(
                WIKIPEDIA_SEARCH_URL,
                params={"search": topic},
                headers=REQUEST_HEADERS,
                timeout=REQUEST_TIMEOUT_SECONDS,
            )
        except requests.exceptions.Timeout as error:
            raise WikipediaTimeoutError(
                "La solicitud a Wikipedia ha expirado. Inténtalo de nuevo."
            ) from error
        except requests.exceptions.ConnectionError as error:
            raise WikipediaConnectionError(
                "No se pudo conectar con Wikipedia. Verifica tu conexión a internet."
            ) from error
        if not response.ok:
            raise WikipediaConnectionError(
                "Wikipedia no pudo atender la solicitud. Inténtalo más tarde."
            )
        if self._is_search_results_page(response):
            raise TopicNotFoundError(
                f"No se encontró ningún artículo en Wikipedia para: '{topic}'."
            )
        return response.text

    def _is_search_results_page(self, response) -> bool:
        return SEARCH_RESULTS_URL_MARKER in response.url
