from unittest.mock import patch

import pytest
import requests
from pytest_bdd import given, parsers, scenarios, then, when

from src.scraper import ArticleParser, ScraperError, WikipediaScraper

scenarios("features/scraper.feature")


def build_wikipedia_html(title, paragraphs):
    paragraph_tags = "".join(f"<p>{text}</p>" for text in paragraphs)
    return (
        f'<html><body><h1 id="firstHeading">{title}</h1>'
        f'<div id="mw-content-text"><div class="mw-parser-output">{paragraph_tags}</div></div>'
        "</body></html>"
    )


@given(
    parsers.parse('a Wikipedia page titled "{title}" with {count:d} paragraphs'),
    target_fixture="html",
)
def page_with_paragraphs(title, count):
    paragraphs = [f"Paragraph number {number}." for number in range(1, count + 1)]
    return build_wikipedia_html(title, paragraphs)


@given(
    "a Wikipedia page with an empty paragraph before two real paragraphs",
    target_fixture="html",
)
def page_with_empty_paragraph():
    return build_wikipedia_html(
        "Python", ["", "First real paragraph.", "Second real paragraph."]
    )


@given(
    "a Wikipedia page with a paragraph containing a citation marker",
    target_fixture="html",
)
def page_with_citation_marker():
    return build_wikipedia_html("Python", ["Python is a language<sup>[1]</sup>."])


@when("the page is parsed", target_fixture="article")
def parse_page(html):
    return ArticleParser().parse(html)


@then(parsers.parse('the article title is "{expected_title}"'))
def check_title(article, expected_title):
    assert article.title == expected_title


@then(parsers.parse("the article has {expected_count:d} paragraphs"))
def check_paragraph_count(article, expected_count):
    assert len(article.paragraphs) == expected_count


@then(parsers.parse('the first paragraph is "{expected_text}"'))
def check_first_paragraph(article, expected_text):
    assert article.paragraphs[0] == expected_text

@pytest.fixture
def mocked_get():
    with patch("src.scraper.requests.get") as mocked:
        yield mocked


@given(parsers.parse('Wikipedia answers with a page titled "{title}"'))
def wikipedia_answers(mocked_get, title):
    mocked_get.return_value.text = build_wikipedia_html(title, ["Some content."])


@when(parsers.parse('the user searches for "{topic}"'), target_fixture="article")
def search_topic(topic):
    return WikipediaScraper().search(topic)


@then(parsers.parse('Wikipedia was queried with the topic "{topic}"'))
def check_wikipedia_query(mocked_get, topic):
    assert mocked_get.call_args.kwargs["params"] == {"search": topic}

@given(
    "a Wikipedia page with its paragraphs wrapped in sections",
    target_fixture="html",
)
def page_with_sections():
    return (
        '<html><body><h1 id="firstHeading">Python</h1>'
        '<div id="mw-content-text"><div class="mw-parser-output">'
        "<section><p>First paragraph.</p><p>Second paragraph.</p></section>"
        "</div></div></body></html>"
    )


@given("Wikipedia answers with a search results page")
def wikipedia_answers_search_results(mocked_get):
    mocked_get.return_value.url = (
        "https://es.wikipedia.org/w/index.php?search=zzz&title=Especial:Buscar"
    )


@given(parsers.parse("Wikipedia answers with the status {status_code:d}"))
def wikipedia_answers_with_status(mocked_get, status_code):
    mocked_get.return_value.status_code = status_code
    mocked_get.return_value.ok = status_code < 400


@given("the connection to Wikipedia fails")
def connection_fails(mocked_get):
    mocked_get.side_effect = requests.exceptions.ConnectionError()


@given("Wikipedia takes too long to answer")
def wikipedia_times_out(mocked_get):
    mocked_get.side_effect = requests.exceptions.Timeout()


@given("Wikipedia answers with an article without paragraphs")
def wikipedia_answers_empty_article(mocked_get):
    mocked_get.return_value.text = build_wikipedia_html("Python", [])


@when(
    parsers.parse('the user tries to search for "{topic}"'),
    target_fixture="search_error",
)
def search_topic_and_fail(topic):
    with pytest.raises(ScraperError) as error_info:
        WikipediaScraper().search(topic)
    return error_info.value


@then(parsers.parse('the error message contains "{expected_text}"'))
def check_error_message(search_error, expected_text):
    assert expected_text in str(search_error)