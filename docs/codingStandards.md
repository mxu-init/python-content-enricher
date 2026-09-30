# Guía de Estándares y Convenciones de Desarrollo Web

Este documento establece las normas obligatorias de desarrollo y organización del código para el equipo. Su cumplimiento es **estricto** para garantizar la mantenibilidad, escalabilidad y coherencia de todos nuestros proyectos React/Vite.

---

## 1. Nomenclatura, Idioma y Contenido de Usuario

* **Idioma de Código:** Todo el código fuente (variables, funciones, clases, nombres de archivos, carpetas y commits) debe estar escrito en **inglés**.
* **Idioma de Interfaz (UI):** Todo el contenido visible para el usuario final debe estar obligatoriamente en **español**.
* **Archivos y Variables Generales:** Nombres en `snake_case` (ej. `user_data`, `product_card_img.jpg`).

---

## 2. Estructura de Proyecto y Carpeteo

La arquitectura del proyecto sigue un enfoque modular basado en componentes, páginas y servicios.

```text
src/
├── assets/             # Imágenes y recursos estáticos locales
├── components/         # Componentes reutilizables de UI (Carpetas en PascalCase)
│   └── Header/
│       ├── Header.jsx
│       └── Header.css
├── pages/              # Páginas o vistas principales (Carpetas en minúsculas)
│   └── products/
│       ├── Products.jsx
│       └── Products.css
├── services/           # Capa de API y peticiones HTTP centralizadas
│   ├── api.js          # Instancia base de Axios e interceptores
│   └── productService.js
├── index.css           # Estilos globales de la aplicación
└── main.jsx            # Punto de entrada de la aplicación

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