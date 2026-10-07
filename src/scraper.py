import requests
from bs4 import BeautifulSoup

class WikipediaScraper:
    def __init__(self, topic: str):
        self.topic = topic
        self.base_url = "https://es.wikipedia.org/wiki/"

    def fetch_content(self) -> dict:
        formatted_topic = self.topic.replace(" ", "_")
        url = f"{self.base_url}{formatted_topic}"
        
        try:
            response = requests.get(url, timeout=10)
            
            if response.status_code == 404:
                print(f"[Error]: No se encontró ningún artículo en Wikipedia para el término ingresado: '{self.topic}'")
                return None
            
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            title_tag = soup.find('h1', id='firstHeading')
            title = title_tag.text if title_tag else self.topic
            
            paragraphs = [p.text for p in soup.select('div.mw-parser-output > p') if p.text.strip()][:5]
            
            if not paragraphs:
                print(f"[Error]: El artículo '{self.topic}' no contiene suficiente información de contenido.")
                return None
                
            return {"title": title, "paragraphs": paragraphs}

        