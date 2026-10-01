# Guía de Estándares y Convenciones de Desarrollo Web

Este documento establece las normas obligatorias de desarrollo y organización del código para el equipo. Su cumplimiento es **estricto** para garantizar la mantenibilidad, escalabilidad y coherencia de todos nuestros proyectos React/Vite.

---

## 1. Nomenclatura, Idioma y Contenido de Usuario

* **Idioma de Código:** Todo el código fuente (variables, funciones, clases, nombres de archivos, carpetas y commits) debe estar escrito en **inglés**.
* **Idioma de Interfaz (UI):** Todo el contenido visible para el usuario final debe estar obligatoriamente en **español**.
* **Archivos y Variables Generales:** Nombres en `snake_case` (ej. `user_data`, `product_card_img.jpg`).
* **Conventional commits y branches:**

---

## 2. Estructura de Proyecto y Carpeteo
```text
content-enricher/
├── .github/
│   └── workflows/
│       └── ci.yml               # Pipeline de integración continua (CI)
├── logs/
│   └── .gitkeep                 # Carpeta reservada para archivos de log
├── output/
│   └── .gitkeep                 # Carpeta de salida para documentos PDF/TXT
├── src/
│   ├── __init__.py
│   ├── logger_config.py         # Configuración del sistema de trazabilidad/logs
│   ├── scraper.py               # Extracción web con BeautifulSoup y Requests
│   ├── enricher.py              # Integración con OpenAI GPT (Enriquecimiento y Resumen)
│   ├── translator.py            # Traducción multi-idioma con Deep Translator
│   ├── exporter.py              # Estrategias de exportación (ReportLab PDF y TXT)
│   └── main.py                  # Orquestador principal e interfaz de usuario (CLI)
├── tests/
│   ├── __init__.py
│   ├── features/
│   │   └── enricher.feature     # Casos de prueba en sintaxis Gherkin (BDD)
│   ├── test_scraper.py          # Pruebas unitarias e integración del módulo Scraper
│   ├── test_enricher.py         # Pruebas unitarias del módulo AI Enricher
│   ├── test_translator.py       # Pruebas unitarias del módulo Translator
│   └── test_exporter.py         # Pruebas unitarias del módulo Exporter
├── .gitignore                   # Exclusión de archivos temporales y credenciales
├── pytest.ini                   # Configuración global para Pytest y Pytest-BDD
├── requirements.txt             # Dependencias del proyecto
└── README.md                    # Documentación principal del proyecto
```
---

## 3. Código Limpio y Sin Comentarios (Clean Code)

* **Prohibido el uso de comentarios:** El código debe ser autoexplicativo por sí mismo. Si una función o variable requiere un comentario para entenderse, debe ser refactorizada o renombrada para expresar su intención con claridad.
* **Funciones pequeñas y de responsabilidad única (Single Responsibility Principle):** Cada función debe hacer solo una cosa y hacerla bien.
* **Nombres descriptivos y con sentido:**
* Usa nombres precisos para funciones y variables en inglés (ej. `fetch_user_profile` en lugar de `get_data`, `is_user_logged_in` en lugar de `flag`).
* Evita abreviaturas confusas (ej. `product_index` en lugar de `idx` o `p`).


* **Manejo de condicionales:** Prioriza retornos tempranos (*early returns*) y guardas (*guard clauses*) para evitar anidamientos profundos de estructuras `if-else`.
* **Código muerto y variables sin usar:** Queda totalmente prohibido dejar código comentado, funciones no utilizadas o importaciones no requeridas en los archivos entregados.


---

## 4. Tecnologías, Librerías y Enrutado

El stack oficial del proyecto está fijado. No se deben añadir librerías adicionales para resolver tareas cubiertas por el stack base sin la aprobación previa del equipo.

* **Lenguaje:** JavaScript (ES6+).
* **Entorno / Bundler:** Vite.
* **Consumo de APIs:** Axios.
* **Linter y Calidad:** ESLint (debe ejecutarse sin errores antes de cada subida a producción o PR).
* **Enrutado (`react-router-dom`):**
* Las rutas definidas en el atributo `path` deben seguir estrictamente la convención estándar en **`kebab-case`** (letras minúsculas separadas por guiones).
* *Ejemplos:*
* `<Route element="{<UserProfile" path="/user-profile"/>} />`
* `<Route element="{<ProductDetails" path="/product-details/:id"/>} />`


---

## 6. Buenas Prácticas