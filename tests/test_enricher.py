from unittest.mock import MagicMock, patch

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from src.enricher import (
    ENRICHMENT_FALLBACK,
    MISSING_KEY_FALLBACK,
    GeminiContentEnricher,
)

scenarios("features/enricher.feature")


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def enrichment_result():
    return {"text": ""}


# ---------------------------------------------------------------------------
# BDD step definitions
# ---------------------------------------------------------------------------


@given(
    parsers.parse('a working Gemini client that returns "{response_text}"'),
    target_fixture="enricher",
)
def enricher_with_working_client(response_text):
    with patch("src.enricher.genai.Client") as mock_client_class:
        mock_response = MagicMock()
        mock_response.text = response_text
        mock_client_class.return_value.models.generate_content.return_value = mock_response
        enricher = GeminiContentEnricher.__new__(GeminiContentEnricher)
        enricher.logger = MagicMock()
        enricher._api_key = "fake-key"
        enricher._client = mock_client_class.return_value
        yield enricher


@given("a Gemini client that raises an exception", target_fixture="enricher")
def enricher_with_failing_client():
    mock_client = MagicMock()
    mock_client.models.generate_content.side_effect = Exception("network error")
    enricher = GeminiContentEnricher.__new__(GeminiContentEnricher)
    enricher.logger = MagicMock()
    enricher._api_key = "fake-key"
    enricher._client = mock_client
    return enricher


@given("no API key is configured", target_fixture="enricher")
def enricher_without_api_key():
    enricher = GeminiContentEnricher.__new__(GeminiContentEnricher)
    enricher.logger = MagicMock()
    enricher._api_key = None
    enricher._client = None
    return enricher


@when(
    parsers.parse('I enrich the article titled "{title}" with "{text}"'),
    target_fixture="enrichment_result",
)
def enrich_article(enricher, title, text):
    return {"text": enricher.enrich_content(title, text)}


@then(parsers.parse('the enriched result is "{expected}"'))
def check_exact_result(enrichment_result, expected):
    assert enrichment_result["text"] == expected


@then(parsers.parse('the enriched result contains "{fragment}"'))
def check_result_contains(enrichment_result, fragment):
    assert fragment in enrichment_result["text"]


# ---------------------------------------------------------------------------
# Unit tests (non-BDD) for 100% coverage
# ---------------------------------------------------------------------------


def test_setup_logger_creates_handler():
    from src.enricher import setup_logger
    logger = setup_logger()
    assert logger.name == "enricher"
    assert len(logger.handlers) >= 1


def test_setup_logger_idempotent():
    from src.enricher import setup_logger
    first = setup_logger()
    handler_count = len(first.handlers)
    second = setup_logger()
    assert len(second.handlers) == handler_count


def test_build_client_returns_none_when_no_key():
    enricher = GeminiContentEnricher.__new__(GeminiContentEnricher)
    enricher.logger = MagicMock()
    enricher._api_key = None
    result = enricher._build_client()
    assert result is None
    enricher.logger.warning.assert_called_once()


def test_build_client_creates_genai_client_when_key_present():
    with patch("src.enricher.genai.Client") as mock_client_class:
        mock_client_class.return_value = MagicMock()
        enricher = GeminiContentEnricher.__new__(GeminiContentEnricher)
        enricher.logger = MagicMock()
        enricher._api_key = "fake-key"
        result = enricher._build_client()
        assert result is mock_client_class.return_value
        mock_client_class.assert_called_once()


def test_build_prompt_contains_title_and_text():
    enricher = GeminiContentEnricher.__new__(GeminiContentEnricher)
    enricher.logger = MagicMock()
    prompt = enricher._build_prompt("Python", "Python es un lenguaje.")
    assert "Python" in prompt
    assert "Python es un lenguaje." in prompt


def test_enrich_content_returns_missing_key_fallback_when_no_client():
    enricher = GeminiContentEnricher.__new__(GeminiContentEnricher)
    enricher.logger = MagicMock()
    enricher._api_key = None
    enricher._client = None
    result = enricher.enrich_content("Python", "Texto.")
    assert result == MISSING_KEY_FALLBACK


def test_enrich_content_returns_enrichment_fallback_on_exception():
    mock_client = MagicMock()
    mock_client.models.generate_content.side_effect = Exception("timeout")
    enricher = GeminiContentEnricher.__new__(GeminiContentEnricher)
    enricher.logger = MagicMock()
    enricher._api_key = "fake-key"
    enricher._client = mock_client
    result = enricher.enrich_content("Python", "Texto.")
    assert result == ENRICHMENT_FALLBACK


def test_enrich_content_returns_model_text_on_success():
    mock_response = MagicMock()
    mock_response.text = "Respuesta enriquecida."
    mock_client = MagicMock()
    mock_client.models.generate_content.return_value = mock_response
    enricher = GeminiContentEnricher.__new__(GeminiContentEnricher)
    enricher.logger = MagicMock()
    enricher._api_key = "fake-key"
    enricher._client = mock_client
    result = enricher.enrich_content("Python", "Texto.")
    assert result == "Respuesta enriquecida."


def test_init_with_no_key_sets_client_to_none():
    with patch("src.enricher.load_dotenv"), patch("src.enricher.os.getenv", return_value=None):
        enricher = GeminiContentEnricher()
    assert enricher._client is None
    assert enricher._api_key is None


def test_init_with_key_creates_client():
    mock_client_instance = MagicMock()
    with (
        patch("src.enricher.load_dotenv"),
        patch("src.enricher.os.getenv", return_value="fake-key"),
        patch("src.enricher.genai.Client", return_value=mock_client_instance),
    ):
        enricher = GeminiContentEnricher()
    assert enricher._client is mock_client_instance
