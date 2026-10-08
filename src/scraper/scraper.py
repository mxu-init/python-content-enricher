import requests
from bs4 import BeautifulSoup
from typing import Dict, List

class WikipediaScraper:
    """Clase encargada exclusivamente de la extracción de información desde Wikipedia."""

    BASE_URL = "https://es.wikipedia.org/wiki/"

    def __init__(self, logger):
        self.logger = logger

    def fetch_article(self, topic: str) -> Dict[str, str]:
        formatted_topic = topic.strip().replace(" ", "_")
        url = f"{self.BASE_URL}{formatted_topic}"
        self.logger.info(f"Iniciando scraping en URL: {url}")

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 (ContentEnricherBot/1.0)"
        }

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            self.logger.error(f"Error de conexión al obtener el artículo '{topic}': {e}")
            raise RuntimeError(f"No se pudo acceder a Wikipedia para el tema: {topic}")

        soup = BeautifulSoup(response.content, "html.parser")

        # Obtener título
        title_tag = soup.find("h1", id="firstHeading")
        title = title_tag.text.strip() if title_tag else topic

        # Extraer párrafos con contenido textual real
        paragraphs: List[str] = []
        for p in soup.select("div.mw-parser-output p"):
            text = p.get_text().strip()
            if text and len(text) > 30:  # Filtrar párrafos vacíos o diminutos
                paragraphs.append(text)
            if len(paragraphs) == 5:
                break

        if not paragraphs:
            self.logger.warning(f"No se encontraron párrafos válidos para '{topic}'.")
            raise ValueError(f"El artículo '{topic}' no contiene suficiente texto.")

        full_text = "\n\n".join(paragraphs)
        self.logger.info(f"Scraping completado con éxito. Se extrajeron {len(paragraphs)} párrafos.")

        return {
            "title": title,
            "original_text": full_text,
            "paragraphs": paragraphs
        }