Feature: AI content enrichment with Gemini
  As a student
  I want my scraped article to be enriched by Gemini
  So that I can study complex topics more easily

  Scenario: Enrich content successfully with a mocked Gemini client
    Given a working Gemini client that returns "Contenido enriquecido por IA."
    When I enrich the article titled "Python" with "Python es un lenguaje."
    Then the enriched result is "Contenido enriquecido por IA."

  Scenario: Return fallback when Gemini raises an exception
    Given a Gemini client that raises an exception
    When I enrich the article titled "Python" with "Python es un lenguaje."
    Then the enriched result contains "[Enriquecimiento no disponible"

  Scenario: Return fallback when GEMINI_API_KEY is missing
    Given no API key is configured
    When I enrich the article titled "Python" with "Python es un lenguaje."
    Then the enriched result contains "falta la clave GEMINI_API_KEY"