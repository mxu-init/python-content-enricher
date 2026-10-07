import requests
from bs4 import BeautifulSoup

class WikipediaScraper:
    def __init__(self, topic: str):
        self.topic = topic
        self.base_url = "https://es.wikipedia.org/wiki/"