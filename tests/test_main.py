from unittest.mock import patch
from pathlib import Path

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from src.exporters import ExportError
from src.main import CliInput, CliOutput, ContentEnricherApp, UserRequest
from src.scraper import ScraperError, WikipediaArticle
from src.translator import TranslationError
from src.summarizer import (
    ArticleSummary,
    CONNECTION_ERROR_MESSAGE,
    SummaryGenerationError,
)

scenarios("features/main.feature")
pytestmark = pytest.mark.usefixtures("capsys")


@pytest.fixture
def typed_answers():
    return []


@pytest.fixture
def screen_output():
    return {"text": ""}


@given(parsers.re(r'the user types "(?P<answer>.*)"'))
def user_types(typed_answers, answer):
    typed_answers.append(answer)


@when("the request is asked", target_fixture="user_request")
def ask_request(typed_answers):
    with patch("builtins.input", side_effect=typed_answers):
        return CliInput().ask_request()


@then(parsers.parse('the request topic is "{expected_topic}"'))
def check_topic(user_request, expected_topic):
    assert user_request.topic == expected_topic


@then(parsers.parse('the request language is "{expected_language}"'))
def check_language(user_request, expected_language):
    assert user_request.language == expected_language


@then("the request wants a summary")
def check_wants_summary(user_request):
    assert user_request.wants_summary is True


@then("the request does not want a summary")
def check_does_not_want_summary(user_request):
    assert user_request.wants_summary is False


@then(parsers.parse('the screen shows "{expected_text}"'))
def check_screen(capsys, screen_output, expected_text):
    screen_output["text"] += capsys.readouterr().out
    assert expected_text in screen_output["text"]


@pytest.fixture
def mocked_scraper():
    with patch("src.main.WikipediaScraper") as scraper_class:
        yield scraper_class.return_value


@pytest.fixture
def mocked_enricher():
    with patch("src.main.GeminiContentEnricher") as enricher_class:
        enricher_class.return_value.enrich_content.return_value = "[mocked enrichment]"
        yield enricher_class.return_value


@pytest.fixture(autouse=True)
def mocked_translator():
    with patch("src.main.ContentTranslator") as translator_class:
        translator_class.return_value.translate.return_value = "Translated content."
        yield translator_class.return_value


@pytest.fixture
def mocked_summarizer():
    with patch("src.main.ArticleSummarizer") as summarizer_class:
        yield summarizer_class.return_value


@pytest.fixture
def mocked_txt_exporter():
    with patch("src.main.TxtExporter") as exporter_class:
        yield exporter_class.return_value


@pytest.fixture
def mocked_pdf_exporter():
    with patch("src.main.PdfExporter") as exporter_class:
        yield exporter_class.return_value


@given(
    parsers.parse(
        'an article titled "{title}" with the paragraphs "{first}" and "{second}"'
    ),
    target_fixture="article",
)
def article_with_paragraphs(title, first, second):
    return WikipediaArticle(title=title, paragraphs=[first, second])


@given(parsers.parse('Wikipedia answers with the article "{title}"'))
def wikipedia_answers(mocked_scraper, title):
    mocked_scraper.search.return_value = WikipediaArticle(
        title=title, paragraphs=["Some content."]
    )


@given(parsers.parse('Wikipedia answers with an empty article titled "{title}"'))
def wikipedia_answers_empty(mocked_scraper, title):
    mocked_scraper.search.return_value = WikipediaArticle(title=title, paragraphs=[])


@given("the summary is generated successfully")
def summary_generated_successfully(mocked_summarizer):
    mocked_summarizer.summarize.return_value = ArticleSummary(
        title="Python", text="Resumen de prueba."
    )


@given("the summary is saved successfully")
def summary_saved_successfully(mocked_txt_exporter):
    mocked_txt_exporter.export_summary.return_value = Path("output/python_summary.txt")


@given("the export always fails")
def export_always_fails(mocked_txt_exporter):
    mocked_txt_exporter.export_summary.side_effect = ExportError(
        "No se pudo guardar el resumen."
    )


@given("the summary cannot be generated")
def summary_cannot_be_generated(mocked_summarizer):
    mocked_summarizer.summarize.side_effect = SummaryGenerationError(
        "No se pudo generar el resumen."
    )


@given("Gemini is not available")
def gemini_not_available(mocked_summarizer):
    mocked_summarizer.summarize.side_effect = SummaryGenerationError(
        CONNECTION_ERROR_MESSAGE
    )


@when("the article is shown")
def show_article(article):
    CliOutput().show_article(article)


@when("the application runs")
def run_application(typed_answers, mocked_scraper, mocked_enricher):
    with patch("builtins.input", side_effect=typed_answers):
        ContentEnricherApp().run()


@then(parsers.parse('Wikipedia was searched for "{topic}"'))
def check_search(mocked_scraper, topic):
    mocked_scraper.search.assert_called_once_with(topic)


@given(parsers.parse('the search fails with the message "{message}"'))
def search_fails(mocked_scraper, message):
    mocked_scraper.search.side_effect = ScraperError(message)


@given(parsers.parse('the translation fails with the message "{message}"'))
def translation_fails(mocked_translator, message):
    mocked_translator.translate.side_effect = TranslationError(message)


@then(parsers.parse('the translator was asked for the language "{language}"'))
def check_translator_language(mocked_translator, language):
    assert mocked_translator.translate.call_args.args[1] == language


def test_ask_export_options():
    cli_input = CliInput()
    with patch("builtins.input", side_effect=["quizas", "s", "", "mi_archivo", "invalid", "txt"]):
        wants, filename, fmt = cli_input._ask_export()
        assert wants is True
        assert filename == "mi_archivo"
        assert fmt == "txt"

    with patch("builtins.input", side_effect=["s", "archivo_pdf", "pdf"]):
        wants, filename, fmt = cli_input._ask_export()
        assert wants is True
        assert filename == "archivo_pdf"
        assert fmt == "pdf"


def test_run_with_full_article_export_txt(mocked_scraper, mocked_enricher, mocked_translator, mocked_txt_exporter):
    mocked_scraper.search.return_value = WikipediaArticle(title="Python", paragraphs=["Contenido"])
    mocked_enricher.enrich_content.return_value = "Enriquecido"
    mocked_translator.translate.return_value = "Traducido"
    mocked_txt_exporter.export.return_value = Path("output/mi_archivo.txt")

    app = ContentEnricherApp()
    with patch.object(app._cli_input, "ask_request", return_value=UserRequest("Python", "en", False, True, "mi_archivo", "txt")):
        app.run()
    mocked_txt_exporter.export.assert_called_once()


def test_run_with_full_article_export_pdf(mocked_scraper, mocked_enricher, mocked_translator, mocked_pdf_exporter):
    mocked_scraper.search.return_value = WikipediaArticle(title="Python", paragraphs=["Contenido"])
    mocked_enricher.enrich_content.return_value = "Enriquecido"
    mocked_translator.translate.return_value = "Traducido"
    mocked_pdf_exporter.export.return_value = Path("output/mi_archivo.pdf")

    app = ContentEnricherApp()
    with patch.object(app._cli_input, "ask_request", return_value=UserRequest("Python", "en", False, True, "mi_archivo", "pdf")):
        app.run()
    mocked_pdf_exporter.export.assert_called_once()


def test_run_with_full_article_export_error(mocked_scraper, mocked_enricher, mocked_translator, mocked_txt_exporter, capsys):
    mocked_scraper.search.return_value = WikipediaArticle(title="Python", paragraphs=["Contenido"])
    mocked_enricher.enrich_content.return_value = "Enriquecido"
    mocked_translator.translate.return_value = "Traducido"
    mocked_txt_exporter.export.side_effect = RuntimeError("Error de disco")

    app = ContentEnricherApp()
    with patch.object(app._cli_input, "ask_request", return_value=UserRequest("Python", "en", False, True, "mi_archivo", "txt")):
        app.run()
    captured = capsys.readouterr().out
    assert "Error al exportar: Error de disco" in captured


def test_run_with_summary_export_pdf(mocked_scraper, mocked_enricher, mocked_translator, mocked_summarizer, mocked_pdf_exporter):
    mocked_scraper.search.return_value = WikipediaArticle(title="Python", paragraphs=["Contenido"])
    mocked_enricher.enrich_content.return_value = "Enriquecido"
    mocked_translator.translate.return_value = "Traducido"
    mocked_summarizer.summarize.return_value = ArticleSummary(title="Python", text="Resumen")
    mocked_pdf_exporter.export_summary.return_value = Path("output/resumen.pdf")

    app = ContentEnricherApp()
    with patch.object(app._cli_input, "ask_request", return_value=UserRequest("Python", "en", True, True, "mi_archivo", "pdf")):
        app.run()
    mocked_pdf_exporter.export_summary.assert_called_once()


def test_cli_input_ask_export():
    cli_input = CliInput()
    with patch("builtins.input", side_effect=["s"]):
        assert cli_input.ask_export() is True
    with patch("builtins.input", side_effect=["invalid", "n"]):
        assert cli_input.ask_export() is False