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