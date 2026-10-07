from unittest.mock import patch

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from src.scraper import ArticleParser, WikipediaScraper

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