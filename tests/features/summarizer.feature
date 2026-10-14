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
    And the project has no .env file
    When the article is summarized with an expected error
    Then the summary error message is "No se pudo generar el resumen: falta la clave de API de Gemini. Por favor, inténtelo más tarde."

  Scenario: Read the API key from a .env file when the environment variable is missing
    Given an article titled "Python" with the paragraphs "Python is a language." and "It is used widely."
    And no Gemini API key is configured
    And a Gemini API key is configured in a .env file
    And Gemini answers with a valid summary
    When the article is summarized
    Then the summary title is "Python"
    And the summary text is "Resumen de prueba."

  Scenario: Fail when the API key is missing from the environment and the .env file
    Given an article titled "Python" with the paragraphs "Python is a language." and "It is used widely."
    And no Gemini API key is configured
    And the project has no .env file
    And Gemini answers with a valid summary
    When the article is summarized with an expected error
    Then the summary error message is "No se pudo generar el resumen: falta la clave de API de Gemini. Por favor, inténtelo más tarde."

  Scenario: Fail when the .env file exists without a Gemini API key
    Given an article titled "Python" with the paragraphs "Python is a language." and "It is used widely."
    And no Gemini API key is configured
    And a .env file without a Gemini API key
    And Gemini answers with a valid summary
    When the article is summarized with an expected error
    Then the summary error message is "No se pudo generar el resumen: falta la clave de API de Gemini. Por favor, inténtelo más tarde."

  Scenario: Fail when Gemini returns an empty summary
    Given an article titled "Python" with the paragraphs "Python is a language." and "It is used widely."
    And a Gemini API key is configured
    And Gemini answers with an empty summary text
    When the article is summarized with an expected error
    Then the summary error message is "Gemini no devolvió un resumen válido. Por favor, inténtelo más tarde."

  Scenario: Map an invalid API key error to a message
    Given an article titled "Python" with the paragraphs "Python is a language." and "It is used widely."
    And a Gemini API key is configured
    And Gemini responds with status 400
    When the article is summarized with an expected error
    Then the summary error message is "La clave de API de Gemini no es válida. Por favor, inténtelo más tarde."

  Scenario: Map a forbidden API key error to a message
    Given an article titled "Python" with the paragraphs "Python is a language." and "It is used widely."
    And a Gemini API key is configured
    And Gemini responds with status 403
    When the article is summarized with an expected error
    Then the summary error message is "La clave de API de Gemini no tiene permiso para usar este modelo. Por favor, inténtelo más tarde."

  Scenario: Map an unavailable model error to a message
    Given an article titled "Python" with the paragraphs "Python is a language." and "It is used widely."
    And a Gemini API key is configured
    And Gemini responds with status 404
    When the article is summarized with an expected error
    Then the summary error message is "El modelo de Gemini solicitado no está disponible. Por favor, inténtelo más tarde."

  Scenario: Map a rate limit error to a message
    Given an article titled "Python" with the paragraphs "Python is a language." and "It is used widely."
    And a Gemini API key is configured
    And Gemini responds with status 429
    When the article is summarized with an expected error
    Then the summary error message is "Se alcanzó el límite de solicitudes de Gemini. Por favor, inténtelo más tarde."

  Scenario: Map an unknown HTTP error to a default message
    Given an article titled "Python" with the paragraphs "Python is a language." and "It is used widely."
    And a Gemini API key is configured
    And Gemini responds with status 503
    When the article is summarized with an expected error
    Then the summary error message is "Gemini no respondió correctamente. Por favor, inténtelo más tarde."

  Scenario: Report a connection error
    Given an article titled "Python" with the paragraphs "Python is a language." and "It is used widely."
    And a Gemini API key is configured
    And Gemini is not reachable
    When the article is summarized with an expected error
    Then the summary error message is "No se pudo conectar con Gemini. Por favor, inténtelo más tarde."