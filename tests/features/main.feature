Feature: Consult a topic from the terminal
  As a student
  I want to type the topic, the language and the summary option in the terminal
  So that I can start my research

  Scenario: Ask for topic, language and summary
    Given the user types "Python"
    And the user types "en"
    And the user types "s"
    When the request is asked
    Then the request topic is "Python"
    And the request language is "en"
    And the request wants a summary

  Scenario: Ask again when the topic is empty
    Given the user types ""
    And the user types "Python"
    And the user types "en"
    And the user types "n"
    When the request is asked
    Then the screen shows "El tema no puede estar vacío."
    And the request topic is "Python"

  Scenario: Ask again when the language is not valid
    Given the user types "Python"
    And the user types "xx"
    And the user types "fr"
    And the user types "n"
    When the request is asked
    Then the screen shows "Idioma no válido"
    And the request language is "fr"

  Scenario: Ask again when the summary answer is not valid
    Given the user types "Python"
    And the user types "en"
    And the user types "tal"
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
    And Wikipedia answers with the article "Python"
    When the application runs
    Then Wikipedia was searched for "Python"
    And the screen shows "Python"