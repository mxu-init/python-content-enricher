from unittest.mock import patch

import pytest
import requests
from pytest_bdd import given, parsers, scenarios, then, when

from src.translator import (
    MAX_CHUNK_LENGTH,
    MYMEMORY_WARNING,
    ContentTranslator,
    TranslationError,
)

scenarios("features/translator.feature")


@pytest.fixture
def mocked_translation_service():
    with patch("src.translator.MyMemoryTranslator") as translator_class:
        yield translator_class


@given(
    parsers.parse('a translation service that prefixes every text with "{prefix}"')
)
def service_with_prefix(mocked_translation_service, prefix):
    mocked_translation_service.return_value.translate.side_effect = (
        lambda text: f"{prefix}{text}"
    )


@given("a translation service that is not reachable")
def service_not_reachable(mocked_translation_service):
    mocked_translation_service.return_value.translate.side_effect = (
        requests.exceptions.ConnectionError()
    )


@given("a translation service that answers with a daily limit warning")
def service_daily_limit_warning(mocked_translation_service):
    mocked_translation_service.return_value.translate.return_value = (
        f"{MYMEMORY_WARNING}: YOU USED ALL AVAILABLE FREE TRANSLATIONS FOR TODAY"
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
    parsers.parse(
        'a sentence of {length:d} characters is translated to "{language}"'
    ),
    target_fixture="translated_text",
)
def translate_single_long_sentence(length, language):
    sentence = " ".join(["word"] * (length // 5)) + "."
    return ContentTranslator().translate(sentence, language)


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
def check_requested_language(mocked_translation_service, language):
    assert mocked_translation_service.call_args.kwargs["target"] == language


@then(parsers.parse("the translation service received {expected_count:d} requests"))
def check_request_count(mocked_translation_service, expected_count):
    translate = mocked_translation_service.return_value.translate
    assert translate.call_count == expected_count


@then("no request is longer than the allowed length")
def check_request_length(mocked_translation_service):
    calls = mocked_translation_service.return_value.translate.call_args_list
    assert all(len(call.args[0]) <= MAX_CHUNK_LENGTH for call in calls)


@then(parsers.parse('the error message contains "{expected_text}"'))
def check_error_message(translation_error, expected_text):
    assert expected_text in str(translation_error)
