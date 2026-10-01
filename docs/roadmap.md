## Roadmap

**Épica 1 · Setup y gestión**
1. Crear repo en GitHub con gitflow (`main`/`develop`), plantilla de PR y README base
2. Estructura del proyecto, `requirements.txt` y configuración de pytest
3. Montar el tablero Kanban y asignar roles (PO, SM, devs)
4. Redactar historias de usuario con criterios de aceptación
5. Product backlog con roadmap y sprint backlog con estimaciones
6. Flowchart de los algoritmos (según el flujo de proceso)

**Épica 2 · Scraping de Wikipedia**
7. Clase `WikipediaScraper`: búsqueda del tema con Requests
8. Extraer título y primeros 5 párrafos con BeautifulSoup
9. Manejo de errores: tema no encontrado, sin conexión, timeout

**Épica 3 · Interacción por terminal**
10. `CliInput`: pedir tema e idioma con validación
11. Mostrar el contenido original en terminal antes de continuar
12. `MainMenu`: flujo de acciones tras mostrar resultados

**Épica 4 · Enriquecimiento con IA**
13. Clase `AiEnricher`: conexión con la API de IA y prompt de enriquecimiento
14. Mostrar el texto enriquecido y manejar errores de API (clave, límite, vacío)
15. ⭐ Generar resúmenes del contenido enriquecido

**Épica 5 · Traducción**
16. Clase `ContentTranslator` con DeepTranslate
17. Mostrar el texto traducido y manejar idioma no soportado o fallo de API

**Épica 6 · Generación de archivos**
18. `TxtExporter`: guardar original, enriquecido y traducido en .txt
19. `PdfExporter`: lo mismo en .pdf (ReportLab)
20. Elegir nombre de archivo y formato (.txt/.pdf) con validación

**Épica 7 · Logs** ⭐
21. Configurar `AppLogger` con archivo de log
22. Registrar los pasos del proceso y los errores

**Épica 8 · Testing**
23. Tests unitarios del scraper (éxito y fallo)
24. Tests unitarios de IA y traducción con mocks
25. Tests unitarios de CLI y exportadores
26. Test de integración del flujo completo
27. Documentar casos en Gherkin (success y failed)
28. Alcanzar y verificar 100 % de cobertura

**Épica 9 · Entrega**
29. README completo: descripción, dependencias, instalación y uso
30. Preparar la presentación de 15 min y la demo