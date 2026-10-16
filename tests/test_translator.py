from unittest.mock import patch

import pytest
import requests
from pytest_bdd import given, parsers, scenarios, then, when

from src.translator import MAX_CHUNK_LENGTH, ContentTranslator, TranslationError

scenarios("features/translator.feature")


@pytest.fixture
def mocked_google_translator():
    with patch("src.translator.GoogleTranslator") as translator_class:
        yield translator_class


@given(
    parsers.parse('a translation service that prefixes every text with "{prefix}"')
)
def service_with_prefix(mocked_google_translator, prefix):
    mocked_google_translator.return_value.translate.side_effect = (
        lambda text: f"{prefix}{text}"
    )


@given("a translation service that is not reachable")
def service_not_reachable(mocked_google_translator):
    mocked_google_translator.return_value.translate.side_effect = (
        requests.exceptions.ConnectionError()
    )


@when(
    parsers.parse('the text "{text}" is translated to "{language}"'),
    target_fixture="translated_text",
)
def translate_text(text, language):
    return ContentTranslator().translate(text, language)


@when(
    parsers.parse('a text with {count:d} paragraphs is translated to "{language}"'),
    target_fixture="translated_text",
)
def translate_paragraphs(count, language):
    text = "\n\n".join(f"Párrafo {number}." for number in range(1, count + 1))
    return ContentTranslator().translate(text, language)


@when(
    parsers.parse(
        'a paragraph with {count:d} sentences of {length:d} characters is translated to "{language}"'
    ),
    target_fixture="translated_text",
)
def translate_long_paragraph(count, length, language):
    sentence = "a" * (length - 1) + "."
    return ContentTranslator().translate(" ".join([sentence] * count), language)


@when(
    parsers.parse('translating the text "{text}" to "{language}" fails'),
    target_fixture="translation_error",
)
def translate_text_and_fail(text, language):
    with pytest.raises(TranslationError) as error_info:
        ContentTranslator().translate(text, language)
    return error_info.value


@then(parsers.parse('the translated text is "{expected_text}"'))
def check_translated_text(translated_text, expected_text):
    assert translated_text == expected_text


@then(parsers.parse("the translated text has {expected_count:d} paragraphs"))
def check_paragraph_count(translated_text, expected_count):
    assert len(translated_text.split("\n\n")) == expected_count


@then(parsers.parse('the translation service was asked for the language "{language}"'))
def check_requested_language(mocked_google_translator, language):
    assert mocked_google_translator.call_args.kwargs["target"] == language


@then(parsers.parse("the translation service received {expected_count:d} requests"))
def check_request_count(mocked_google_translator, expected_count):
    translate = mocked_google_translator.return_value.translate
    assert translate.call_count == expected_count


@then("no request is longer than the allowed length")
def check_request_length(mocked_google_translator):
    calls = mocked_google_translator.return_value.translate.call_args_list
    assert all(len(call.args[0]) <= MAX_CHUNK_LENGTH for call in calls)


@then(parsers.parse('the error message contains "{expected_text}"'))
def check_error_message(translation_error, expected_text):
    assert expected_text in str(translation_error)
