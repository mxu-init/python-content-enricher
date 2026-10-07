import sys
from dotenv import load_dotenv
from src.logger.logger_config import setup_logger
from src.scraper.scraper import WikipediaScraper
from src.enricher.enricher import AIEnricher
from src.translator.translator import DeepTranslatorService
from src.exporter.exporter import TextExporter, PdfExporter

load_dotenv()  # Carga las variables definidas en el archivo .env

class ContentEnricherApp:
    """Clase principal que orquesta el flujo completo de la aplicación."""

    def __init__(self):
        self.logger = setup_logger()
        self.scraper = WikipediaScraper(self.logger)
        self.enricher = AIEnricher(self.logger)
        self.translator = DeepTranslatorService(self.logger)

    def run(self):
        print("\n=== Sistema Content Enricher ===")
        self.logger.info("Aplicación iniciada por el usuario.")

        try:
            # 1. Entrada de datos por consola
            topic = input(" Ingrese el tema a investigar: ").strip()
            if not topic:
                print("El tema no puede estar vacío.")
                return

            lang = input(" Ingrese el código del idioma para la traducción (ej. en, fr, de, it): ").strip().lower()
            if not lang:
                lang = "en"

            # 2. Scraping de Wikipedia
            print("\n[1/4] Buscando en Wikipedia...")
            wiki_data = self.scraper.fetch_article(topic)

            print("\n" + "="*50)
            print(f" TÍTULO ENCONTRADO: {wiki_data['title']}")
            print("="*50)
            print(" CONTENIDO ORIGINAL (Primeros 5 párrafos):")
            print(wiki_data['original_text'])
            print("="*50)

            # 3. Enriquecimiento y Resumen
            print("\n[2/4] Enriqueciendo contenido con IA...")
            enriched_text = self.enricher.enrich_content(wiki_data['title'], wiki_data['original_text'])

            print("\n Generating Resumen...")
            summary_text = self.enricher.generate_summary(enriched_text)

            print("\n" + "="*50)
            print(" CONTENIDO ENRIQUECIDO:")
            print(enriched_text)
            print("\n RESUMEN EJECUTIVO:")
            print(summary_text)
            print("="*50)

            # 4. Traducción
            print(f"\n[3/4] Traduciendo contenido al idioma '{lang}'...")
            translated_text = self.translator.translate(enriched_text, target_language=lang)

            print("\n" + "="*50)
            print(f" CONTENIDO TRADUCIDO ({lang.upper()}):")
            print(translated_text)
            print("="*50)

            # 5. Generación de Archivos
            print("\n[4/4] Opciones de exportación")
            format_choice = input(" Elija formato de salida (pdf / txt): ").strip().lower()
            file_name = input(" Ingrese el nombre para el archivo (sin extensión): ").strip()

            if not file_name:
                file_name = f"informe_{topic.replace(' ', '_')}"

            if format_choice == "pdf":
                exporter = PdfExporter(self.logger)
            else:
                exporter = TextExporter(self.logger)

            file_path = exporter.export(
                filename=file_name,
                title=wiki_data['title'],
                original=wiki_data['original_text'],
                enriched=enriched_text,
                summary=summary_text,
                translated=translated_text
            )

            print(f"\n ¡Proceso completado con éxito! Archivo guardado en:\n{file_path}\n")

        except Exception as e:
            self.logger.error(f"Error durante la ejecución del programa: {e}")
            print(f"\n Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    app = ContentEnricherApp()
    app.run()