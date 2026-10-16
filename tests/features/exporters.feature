Feature: Exporting content
  As a user
  I want to export the article content to a text or PDF file
  So that I can save it locally and review it later

  Scenario: Exporting article content as a text file
    Given a file name "resultado" and format "txt"
    When the exporter saves the content
    Then the file "resultado.txt" should be created successfully

  Scenario: Exporting article content as a PDF file
    Given a file name "documento" and format "pdf"
    When the exporter saves the content
    Then the file "documento.pdf" should be created successfully