from unittest.mock import patch

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from src.main import CliInput, CliOutput, ContentEnricherApp
from src.scraper import WikipediaArticle

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