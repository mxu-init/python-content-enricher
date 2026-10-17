Feature: Consult a topic from the terminal
  As a student
  I want to type the topic, the language and the summary option in the terminal
  So that I can start my research

  Scenario: Ask for topic, language and summary
    Given the user types "Python"
    And the user types "en"
    And the user types "s"
    And the user types "n"
    When the request is asked
    Then the request topic is "Python"
    And the request language is "en"
    And the request wants a summary

  Scenario: Ask again when the topic is empty
    Given the user types ""
    And the user types "Python"
    And the user types "en"
    And the user types "n"
    And the user types "n"
    When the request is asked
    Then the screen shows "El tema no puede estar vacío."
    And the request topic is "Python"

  Scenario: Ask again when the language is not valid
    Given the user types "Python"
    And the user types "xx"
    And the user types "fr"
    And the user types "n"
    And the user types "n"
    When the request is asked
    Then the screen shows "Idioma no válido"
    And the request language is "fr"

  Scenario: Ask again when the summary answer is not valid
    Given the user types "Python"
    And the user types "en"
    And the user types "tal"
    And the user types "n"
    And the user types "n"
    When the request is asked
    Then the screen shows "Responde con 's' o 'n'."
    And the request does not want a summary


  Scenario: Show the article on screen
    Given an article titled "Python" with the paragraphs "First paragraph." and "Second paragraph."
    When the article is shown
    Then the screen shows "Python"
    And the screen shows "Second paragraph."

  Scenario: Consult a topic from the terminal
    Given the user types "Python"
    And the user types "en"
    And the user types "n"
    And the user types "n"
    And Wikipedia answers with the article "Python"
    When the application runs
    Then Wikipedia was searched for "Python"
    And the screen shows "Python"

  Scenario: Show an error when the search fails
    Given the user types "Tema inexistente"
    And the user types "en"
    And the user types "n"
    And the user types "n"
    And the search fails with the message "No se encontró ningún artículo"
    When the application runs
    Then the screen shows "[Error]: No se encontró ningún artículo"

  Scenario: Show the translation on screen
    Given the user types "Python"
    And the user types "en"
    And the user types "n"
    And the user types "n"
    And Wikipedia answers with the article "Python"
    When the application runs
    Then the screen shows "Translated content."
    And the translator was asked for the language "en"

  Scenario: Show an error when the translation fails
    Given the user types "Python"
    And the user types "en"
    And the user types "n"
    And the user types "n"
    And Wikipedia answers with the article "Python"
    And the translation fails with the message "No se pudo traducir el contenido"
    When the application runs
    Then the screen shows "[Error]: No se pudo traducir el contenido"

  Scenario: Show the summary when it is requested
    Given the user types "Python"
    And the user types "en"
    And the user types "s"
    And the user types "n"
    And the user types "n"
    And Wikipedia answers with the article "Python"
    And the summary is generated successfully
    When the application runs
    Then Wikipedia was searched for "Python"
    And the screen shows "Resumen de prueba."

  Scenario: Save the summary when the export is accepted
    Given the user types "Python"
    And the user types "en"
    And the user types "s"
    And the user types "n"
    And the user types "s"
    And Wikipedia answers with the article "Python"
    And the summary is generated successfully
    And the summary is saved successfully
    When the application runs
    Then Wikipedia was searched for "Python"
    And the screen shows "Resumen guardado en:"

  Scenario: Show a message when the summary cannot be saved
    Given the user types "Python"
    And the user types "en"
    And the user types "s"
    And the user types "n"
    And the user types "s"
    And Wikipedia answers with the article "Python"
    And the summary is generated successfully
    And the export always fails
    When the application runs
    Then Wikipedia was searched for "Python"
    And the screen shows "[Error]: No se pudo guardar el resumen."

  Scenario: Ask again when the export answer is not valid
    Given the user types "Python"
    And the user types "en"
    And the user types "s"
    And the user types "n"
    And the user types "tal"
    And the user types "n"
    And Wikipedia answers with the article "Python"
    And the summary is generated successfully
    When the application runs
    Then the screen shows "Responde con 's' o 'n'."

  Scenario: Show a message when the summary cannot be generated
    Given the user types "Python"
    And the user types "en"
    And the user types "s"
    And the user types "n"
    And Wikipedia answers with the article "Python"
    And the summary cannot be generated
    When the application runs
    Then the screen shows "No se pudo generar el resumen."

  Scenario: Show a friendly message when Gemini is not available
    Given the user types "Python"
    And the user types "en"
    And the user types "s"
    And the user types "n"
    And Wikipedia answers with the article "Python"
    And Gemini is not available
    When the application runs
    Then the screen shows "Por favor, inténtelo más tarde."

  Scenario: Show a message when the article has no content
    Given the user types "Python"
    And the user types "en"
    And the user types "s"
    And the user types "n"
    And Wikipedia answers with an empty article titled "Python"
    When the application runs
    Then the screen shows "No hay contenido suficiente para generar el resumen."