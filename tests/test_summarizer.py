from unittest.mock import patch

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from src.scraper import WikipediaArticle
from src.summarizer import ArticleSummarizer, SummaryGenerationError

scenarios("features/summarizer.feature")


class FakeGeminiError(Exception):
    def __init__(self, status_code):
        super().__init__("fake error")
        self.status_code = status_code


@pytest.fixture
def mocked_client():
    with patch("src.summarizer.genai.Client") as client_class:
        yield client_class.return_value


@given(
    parsers.parse(
        'an article titled "{title}" with the paragraphs "{first}" and "{second}"'
    ),
    target_fixture="article",
)
def article_with_paragraphs(title, first, second):
    return WikipediaArticle(title=title, paragraphs=[first, second])


@given("a Gemini API key is configured")
def gemini_key_configured(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")


@given("no Gemini API key is configured")
def gemini_key_missing(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)


@given("a Gemini API key is configured in a .env file")
def gemini_key_in_env_file(monkeypatch, tmp_path):
    monkeypatch.setattr("src.summarizer.ENV_FILE_DIRECTORY", tmp_path)
    (tmp_path / ".env").write_text('GEMINI_API_KEY="test-key"\n', encoding="utf-8")


@given("a .env file without a Gemini API key")
def env_file_without_gemini_key(monkeypatch, tmp_path):
    monkeypatch.setattr("src.summarizer.ENV_FILE_DIRECTORY", tmp_path)
    (tmp_path / ".env").write_text('OTHER_VAR="value"\n', encoding="utf-8")


@given("the project has no .env file")
def project_without_env_file(monkeypatch, tmp_path):
    monkeypatch.setattr("src.summarizer.ENV_FILE_DIRECTORY", tmp_path)


@given("Gemini answers with a valid summary")
def gemini_valid_answer(mocked_client):
    mocked_client.interactions.create.return_value.output_text = (
        "  Resumen de prueba.  "
    )


@given("Gemini answers with an empty summary text")
def gemini_empty_summary_text(mocked_client):
    mocked_client.interactions.create.return_value.output_text = None


@given(parsers.parse("Gemini responds with status {status_code:d}"))
def gemini_http_error(mocked_client, status_code):
    mocked_client.interactions.create.side_effect = FakeGeminiError(status_code)


@given("Gemini is not reachable")
def gemini_connection_error(mocked_client):
    mocked_client.interactions.create.side_effect = FakeGeminiError(None)


@when("the article is summarized", target_fixture="summary")
def summarize_article(article):
    return ArticleSummarizer().summarize(article)


@when("the article is summarized with an expected error", target_fixture="error_info")
def summarize_with_expected_error(article):
    with pytest.raises(SummaryGenerationError) as error_info:
        ArticleSummarizer().summarize(article)
    return error_info.value


@then(parsers.parse('the summary title is "{expected_title}"'))
def check_summary_title(summary, expected_title):
    assert summary.title == expected_title


@then(parsers.parse('the summary text is "{expected_text}"'))
def check_summary_text(summary, expected_text):
    assert summary.text == expected_text


@then(parsers.parse('the summary error message is "{expected_message}"'))
def check_summary_error(error_info, expected_message):
    assert str(error_info) == expected_message