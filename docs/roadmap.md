# Roadmap · Content Enrichment

Dos sprints. Peso en Story Points (Fibonacci) en historias y tareas.

## Sprint 1 · trabajo el 6 oct · presentación el 7 oct

**Objetivo:** cerrar el setup y mostrar un primer flujo funcional: el usuario escribe un tema y un idioma, y ve el título y el texto de Wikipedia en la terminal, con mensajes claros si algo falla.

**Carga:** 12 puntos de tareas pendientes (el setup ya hecho suma 3 más, ya completados).

| Historia | Tarea | Pts | Estado |
|---|---|---|---|
| Proyecto preparado para trabajar en equipo | Crear repo con gitflow y plantilla de PR | 1 | ✅ hecho |
| | Redactar codingStandards.md | 1 | ✅ hecho |
| | Estructura de carpetas, requirements.txt | 1 | ✅ hecho |
| | Configurar tablero Jira y asignar roles | 1 | pendiente |
| Planificación y diseño documentados | Revisar historias y estimaciones en Jira | 1 | pendiente |
| | Completar el flowchart de los algoritmos pendientes | 1 | hecho |
| Buscar un tema en Wikipedia | WikipediaScraper: búsqueda con Requests | 2 | pendiente |
| | Extraer título y 5 párrafos con BeautifulSoup | 2 | pendiente |
| Consultar un tema desde la terminal | CliInput: tema e idioma con validación | 2 | pendiente |
| | Mostrar título y texto original en terminal | 1 | pendiente |
| Recibir mensajes claros si la búsqueda falla | Excepciones propias y timeout en el scraper | 1 | pendiente |
| | Capturar los errores en la CLI y mostrar el mensaje | 1 | pendiente |

**Orden sugerido para el día 6**
1. Primera hora: tablero Jira y revisión del backlog (rápido, desbloquea el seguimiento).
2. En paralelo: scraper (2 personas), CLI (2 personas)
3. Después: errores del scraper y de la CLI.
4. Al final: unir CLI y scraper, probar el flujo completo y preparar la demo.

**Si falta tiempo:** mover "Recibir mensajes claros si la búsqueda falla" al Sprint 2. Lo imprescindible es el scraper y la CLI.

## Sprint 2 · resto del proyecto

Es un sprint mucho más grande que el primero (37 puntos de tareas), así que conviene priorizar.

| Bloque | Historias | Pts tareas |
|---|---|---|
| Flujo principal | Menú principal · Enriquecer con IA · Traducir · Guardar en .txt/.pdf | 16 |
| Calidad | Tests unitarios · Integración y Gherkin (100 % de cobertura) | 12 |
| Entrega | README y presentación finales | 3 |
| Extras ⭐ | Resumen con IA · Registro en log | 6 |
