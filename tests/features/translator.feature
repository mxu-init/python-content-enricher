Feature: Content translation
  As a student
  I want to translate the content into my chosen language
  So that I can study it in my language

  Scenario: Translate a text into the chosen language
    Given a translation service that prefixes every text with "translated: "
    When the text "Hola mundo" is translated to "fr"
    Then the translated text is "translated: Hola mundo"
    And the translation service was asked for the language "fr-FR"

  Scenario: Keep the paragraphs of the text
    Given a translation service that prefixes every text with "translated: "
    When a text with 3 paragraphs is translated to "en"
    Then the translated text has 3 paragraphs

  Scenario: Split long paragraphs into several requests
    Given a translation service that prefixes every text with "translated: "
    When a paragraph with 2 sentences of 250 characters is translated to "en"
    Then the translation service received 2 requests
    And no request is longer than the allowed length

  Scenario: Split sentences longer than the allowed chunk length
    Given a translation service that prefixes every text with "translated: "
    When a sentence of 600 characters is translated to "en"
    Then the translation service received 2 requests
    And no request is longer than the allowed length

  Scenario: Fail when the translation service is not reachable
    Given a translation service that is not reachable
    When translating the text "Hola mundo" to "fr" fails
    Then the error message contains "No se pudo traducir el contenido"

  Scenario: Fail when the daily translation limit is reached
    Given a translation service that answers with a daily limit warning
    When translating the text "Hola mundo" to "fr" fails
    Then the error message contains "límite de traducción"
