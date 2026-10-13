Feature: Wikipedia article parsing
  As a student
  I want to get the title and the first paragraphs of a Wikipedia article
  So that I can study a topic

  Scenario: Extract the title of an article
    Given a Wikipedia page titled "Python" with 2 paragraphs
    When the page is parsed
    Then the article title is "Python"

  Scenario: Keep only the first five paragraphs
    Given a Wikipedia page titled "Python" with 8 paragraphs
    When the page is parsed
    Then the article has 5 paragraphs

  Scenario: Ignore empty paragraphs
    Given a Wikipedia page with an empty paragraph before two real paragraphs
    When the page is parsed
    Then the article has 2 paragraphs
    And the first paragraph is "First real paragraph."

  Scenario: Remove citation markers
    Given a Wikipedia page with a paragraph containing a citation marker
    When the page is parsed
    Then the first paragraph is "Python is a language."

  Scenario: Search a topic on Wikipedia
    Given Wikipedia answers with a page titled "Python"
    When the user searches for "Python"
    Then the article title is "Python"
    And Wikipedia was queried with the topic "Python"

  Scenario: Read paragraphs wrapped in sections
    Given a Wikipedia page with its paragraphs wrapped in sections
    When the page is parsed
    Then the article has 2 paragraphs

  Scenario: Fail when Wikipedia only shows search results
    Given Wikipedia answers with a search results page
    When the user tries to search for "Tema inexistente"
    Then the error message contains "No se encontró ningún artículo"

  Scenario: Fail when Wikipedia cannot attend the request
    Given Wikipedia answers with the status 500
    When the user tries to search for "Python"
    Then the error message contains "no pudo atender"

  Scenario: Fail when there is no connection
    Given the connection to Wikipedia fails
    When the user tries to search for "Python"
    Then the error message contains "No se pudo conectar"

  Scenario: Fail when Wikipedia takes too long
    Given Wikipedia takes too long to answer
    When the user tries to search for "Python"
    Then the error message contains "ha expirado"

  Scenario: Fail when the article has no content
    Given Wikipedia answers with an article without paragraphs
    When the user tries to search for "Python"
    Then the error message contains "no contiene suficiente información"