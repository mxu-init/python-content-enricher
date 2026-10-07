from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup

WIKIPEDIA_SEARCH_URL = "https://es.wikipedia.org/w/index.php"
REQUEST_HEADERS = {"User-Agent": "ContentEnricher/1.0 (course project)"}
REQUEST_TIMEOUT_SECONDS = 10
PARAGRAPH_LIMIT = 5


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
        paragraph_tags = soup.select("#mw-content-text .mw-parser-output > p")
        texts = [self._clean_paragraph(tag) for tag in paragraph_tags]
        non_empty_texts = [text for text in texts if text]
        return non_empty_texts[:PARAGRAPH_LIMIT]

    def _clean_paragraph(self, paragraph_tag) -> str:
        for citation in paragraph_tag.select("sup"):
            citation.decompose()
        return " ".join(paragraph_tag.get_text().split())