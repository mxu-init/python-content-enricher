Feature: Article summary generation with Gemini
  As a student
  I want to summarize an article with the Gemini API
  So that I can get a concise summary of a topic

  Scenario: Generate a summary from a valid Gemini response
    Given an article titled "Python" with the paragraphs "Python is a language." and "It is used widely."
    And a Gemini API key is configured
    And Gemini answers with a valid summary
    When the article is summarized
    Then the summary title is "Python"
    And the summary text is "Resumen de prueba."

  Scenario: Fail when the API key is missing
    Given an article titled "Python" with the paragraphs "Python is a language." and "It is used widely."
    And no Gemini API key is configured
    When the article is summarized with an expected error
    Then the summary error message is "Falta la variable de entorno GEMINI_API_KEY con tu clave de la API de Gemini."

  Scenario: Fail when Gemini returns an empty summary
    Given an article titled "Python" with the paragraphs "Python is a language." and "It is used widely."
    And a Gemini API key is configured
    And Gemini answers with an empty summary text
    When the article is summarized with an expected error
    Then the summary error message is "Gemini no devolvió un resumen válido."

  Scenario: Map a rate limit error to a message
    Given an article titled "Python" with the paragraphs "Python is a language." and "It is used widely."
    And a Gemini API key is configured
    And Gemini responds with status 429
    When the article is summarized with an expected error
    Then the summary error message is "Se alcanzó el límite del plan gratuito de Gemini. Inténtalo más tarde."

  Scenario: Map an unknown HTTP error to a default message
    Given an article titled "Python" with the paragraphs "Python is a language." and "It is used widely."
    And a Gemini API key is configured
    And Gemini responds with status 503
    When the article is summarized with an expected error
    Then the summary error message is "Gemini respondió con el error 503."

  Scenario: Report a connection error
    Given an article titled "Python" with the paragraphs "Python is a language." and "It is used widely."
    And a Gemini API key is configured
    And Gemini is not reachable
    When the article is summarized with an expected error
    Then the summary error message is "No se pudo conectar con Gemini."