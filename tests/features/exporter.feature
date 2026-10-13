Feature: Export summaries to text files
  As a student
  I want to save the article summary in a text file
  So that I can review the summary later

  Scenario: Save a summary in a text file
    Given a summary titled "Python (lenguaje)" with the text "Resumen de prueba."
    And an output directory
    When the summary is exported
    Then the file is written
    And the file name is "python_lenguaje_summary.txt"
    And the file content starts with "Resumen: Python (lenguaje)"

  Scenario: Use a default file name when the title has no safe characters
    Given a summary titled "???" with the text "Resumen de prueba."
    And an output directory
    When the summary is exported
    Then the file is written
    And the file name is "article_summary.txt"

  Scenario: Report an error when the file cannot be written
    Given a summary titled "Python" with the text "Resumen de prueba."
    And an output directory
    And the file cannot be written
    When the summary is exported with an expected error
    Then the error message contains "No se pudo guardar el resumen en"