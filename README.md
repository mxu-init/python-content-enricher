# 🧠 Content Enricher - Python Pipeline

> Herramienta backend en **Python** diseñada para el enriquecimiento, análisis, resumen y exportación automatizada de contenidos textuales. Desarrollada aplicando estrictamente **TDD (Test-Driven Development)** y pruebas de comportamiento (**BDD**), persiguiendo un objetivo de **100% de cobertura de código**.

---

## 📖 Descripción del Proyecto

**Content Enricher** es una solución modular de procesamiento de lenguaje y contenidos que toma textos o fuentes de información en bruto, los enriquece, extrae sus puntos clave, genera resúmenes optimizados y exporta los resultados enriquecidos y resumidos a múltiples formatos para su investigación y fácil acceso a la información relevante.

### ✨ Funcionalidades Principales
- 🌐 **Scraping de Contenido (`Scraper`):** Búsqueda y extracción de artículos de Wikipedia con limpieza de etiquetas HTML, filtros de párrafos y manejo de errores de conexión.
- 🤖 **Enriquecimiento con IA (`Enricher`):** Enriquecimiento de contenido mediante la API de Google Gemini con gestión de reintentos, políticas de fallback y logs estructurados.
- 🌍 **Traducción Multilingüe (`Translator`):** Traducción del contenido a idiomas soportados (`en`, `fr`, `de`, `it`, `pt`) con división inteligente en fragmentos (*chunks*).
- ⚡ **Resumen Inteligente (`Summarizer`):** Generación de resúmenes ejecutivos del contenido enriquecido utilizando modelos generativos de Gemini.
- 📤 **Exportación Multiformato (`Exporters`):** Generación y guardado de documentos completos y resúmenes en formatos `.txt` y `.pdf` (vía ReportLab) organizados en la ruta `output/`.
- 💻 **Interfaz de Línea de Comandos (CLI):** Flujo interactivo en terminal (`main.py`) con validación de entradas de usuario y presentación formateada.
- 🛡️ **Diseño Robusto y Tolerancia a Fallos:** Manejo controlado de entradas vacías, límites de peticiones, errores de red y excepciones de I/O.

---

## 🧪 Metodología: TDD (Test-Driven Development) & 100% Cobertura

El núcleo de la confiabilidad de este proyecto radica en la adopción del ciclo **Red-Green-Refactor**:

```
 🔴 RED          ➔ Escribir primero un test unitario o escenario que falle.
       ↓
 🟢 GREEN        ➔ Implementar el código mínimo y necesario para superar el test.
       ↓
 🔵 REFACTOR     ➔ Mejorar la arquitectura, modularidad y legibilidad manteniendo los tests en verde.
```

### 🎯 Estrategia Integral de Testing
1. **Pruebas Unitarias Exhaustivas (`pytest`):** Cobertura componente por componente (`test_scraper.py`, `test_enricher.py`, `test_translator.py`, `test_summarizer.py`, `test_exporter.py`, `test_main.py`).
2. **Pruebas de Aceptación / BDD (`tests/features/*.feature`):** Especificaciones en sintaxis Gherkin (*Given-When-Then*) con escenarios ejecutables para cada módulo.
3. **Métricas de Cobertura (`pytest-cov` / `coverage.py`):** Ejecución continua garantizando el **100% de cobertura** de código en todos los componentes del `src/`.

---

## 🛠️ Stack Tecnológico y Librerías

| Categoría | Tecnologías y Herramientas |
| :--- | :--- |
| **Backend & Core** | ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Standard Library](https://img.shields.io/badge/Standard_Library-Python-yellow?style=for-the-badge) |
| **IA & Procesamiento** | ![Google Gemini](https://img.shields.io/badge/Google_Gemini-8E75C2?style=for-the-badge&logo=google&logoColor=white) ![Deep Translator](https://img.shields.io/badge/Deep_Translator-2C3E50?style=for-the-badge) ![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-59666C?style=for-the-badge) ![ReportLab](https://img.shields.io/badge/ReportLab-PDF-red?style=for-the-badge) |
| **Testing & Calidad** | ![Pytest](https://img.shields.io/badge/pytest-%230A9EDC.svg?style=for-the-badge&logo=pytest&logoColor=white) ![Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen?style=for-the-badge) ![BDD](https://img.shields.io/badge/BDD-Gherkin-00A86B?style=for-the-badge) |
| **Metodología** | ![TDD](https://img.shields.io/badge/Metodología-TDD_Test--Driven-red?style=for-the-badge) ![Clean Code](https://img.shields.io/badge/Design-Clean_Code-blue?style=for-the-badge) |

---

## 🧩 Arquitectura del Proyecto

El código está estructurado bajo principios de responsabilidad única (SRP), desacoplamiento y alta cohesión:

```text
content_enricher/
├── src/
│   ├── __init__.py
│   ├── scraper.py             # Búsqueda y extracción de contenido en Wikipedia
│   ├── enricher.py            # Enriquecimiento contextual mediante Google Gemini IA
│   ├── translator.py          # Traducción de contenido multilingüe por fragmentos
│   ├── summarizer.py          # Generación de resúmenes estructurados con Gemini
│   ├── exporters.py           # Exportadores a TXT y PDF (ReportLab) hacia output/
│   └── main.py                # Interfaz CLI interactiva y orquestación del pipeline
├── tests/
│   ├── __init__.py
│   ├── test_scraper.py        # Tests unitarios del scraper de Wikipedia
│   ├── test_enricher.py       # Tests unitarios del enriquecedor con Gemini
│   ├── test_translator.py     # Tests unitarios del traductor multilingüe
│   ├── test_summarizer.py     # Tests unitarios del generador de resúmenes
│   ├── test_exporter.py       # Tests unitarios de los exportadores TXT y PDF
│   ├── test_main.py           # Tests unitarios del flujo CLI y de integración
│   └── features/              # Especificaciones ejecutables BDD (Gherkin)
│       ├── scraper.feature
│       ├── enricher.feature
│       ├── translator.feature
│       ├── summarizer.feature
│       ├── exporter.feature
│       └── main.feature
├── output/                    # Carpeta de destino para archivos exportados (.txt, .pdf)
├── requirements.txt           # Dependencias de producción y testing
├── pytest.ini                 # Configuración de pytest y cobertura
└── README.md                  # Documentación del proyecto
```

### Flujo de Datos
1. **Petición del Usuario:** En `main.py`, la interfaz CLI solicita el tema a investigar, el idioma de traducción, si desea resumen y si desea exportar los resultados.
2. **Scraping:** `scraper.py` consulta Wikipedia, parsea el HTML y extrae los párrafos relevantes del artículo.
3. **Enriquecimiento:** `enricher.py` envía el artículo a la API de Gemini para obtener contenido extendido y enriquecido contextualmente.
4. **Traducción:** `translator.py` divide el contenido enriquecido en fragmentos y lo traduce al idioma solicitado.
5. **Resumen (Opcional):** Si se solicita, `summarizer.py` sintetiza el contenido enriquecido con Gemini en tres párrafos.
6. **Exportación (Opcional):** Si el usuario lo indicó, `exporters.py` guarda en `output/` el documento completo (original, enriquecido y traducido) y el resumen en archivos independientes (formato `.txt` o `.pdf`).

---

## ⚙️ Instalación y Configuración Local

Sigue estos pasos para configurar el entorno virtual y poner en marcha el proyecto:

### 1. Requisitos Previos
- **Python 3.10** o superior instalado en el sistema.
- **Git** para el control de versiones.

### 2. Clonar el Repositorio
```bash
git clone https://github.com/mxu-init/content-enricher.git
```

### 3. Acceder al Directorio
```bash
cd content_enricher
```

### 4. Crear y Activar un Entorno Virtual
- En **Windows (PowerShell)**:
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
- En **Linux / macOS**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 5. Instalar Dependencias
```bash
pip install -r requirements.txt
```

---

## 🧪 Ejecución de Pruebas y Cobertura (TDD)

### Ejecutar la Suite de Pruebas Unitarias
```bash
pytest
```

### Ejecutar con Reporte Detallado de Cobertura
Para comprobar el cumplimiento del objetivo del **100% de cobertura**:
```bash
pytest --cov=src --cov-report=term-missing
```

### Generar Reporte HTML de Cobertura
```bash
pytest --cov=src --cov-report=html
```
*Abre `htmlcov/index.html` en tu navegador para inspeccionar línea a línea la cobertura de cada archivo.*

---

## 👤 Autor

Desarrollado y mantenido por:

| Desarrollador | Perfil de GitHub |
| :--- | :--- |
| **Mauricio Rodríguez** | [@mxu-init](https://github.com/mxu-init) |
| **William Hernandez** | [@wfhgdev ](https://github.com/wfhgdev) |
| **Willfredy Salcedo Silvestre** | [@Willfredy742](https://github.com/Willfredy742) |
| **Jose Loero Nielez** | [@Mltiformacionjose](https://github.com/Mltiformacionjose) |

---
