Feature: Export summaries to text files
  As a student
  I want to save the generated summary in a text file
  So that I can keep a local copy of my research

  Scenario: Save a summary in a text file
    Given a summary titled "Python" with the text "Resumen de prueba."
    When the summary is exported
    Then a text file "python_summary.txt" is created
    And the text file contains the title and the summary

  Scenario: Use a lowercase file name for a title with special characters
    Given a summary titled "Python (lenguaje)" with the text "Resumen de prueba."
    When the summary is exported
    Then a text file "python_lenguaje_summary.txt" is created

  Scenario: Use the default file name when the title has no safe characters
    Given a summary titled "???" with the text "Resumen de prueba."
    When the summary is exported
    Then a text file "article_summary.txt" is created

  Scenario: Report an error when the summary cannot be written
    Given a summary titled "Python" with the text "Resumen de prueba."
    When the summary cannot be exported
    Then an export error is raised
