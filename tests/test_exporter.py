from unittest.mock import patch

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from src.exporter import ExportError, SummaryTextExporter
from src.summarizer import ArticleSummary

scenarios("features/exporter.feature")


@pytest.fixture
def unwritable_file():
    with patch("src.exporter.Path.write_text", side_effect=OSError("disk full")):
        yield


@given(
    parsers.parse('a summary titled "{title}" with the text "{text}"'),
    target_fixture="summary",
)
def summary_with_text(title, text):
    return ArticleSummary(title=title, text=text)


@given("an output directory", target_fixture="exporter")
def exporter_with_output_directory(tmp_path):
    return SummaryTextExporter(output_directory=tmp_path)


@given("the file cannot be written")
def file_cannot_be_written(unwritable_file):
    pass


@when("the summary is exported", target_fixture="exported_path")
def export_summary(exporter, summary):
    return exporter.export(summary)


@when("the summary is exported with an expected error", target_fixture="error")
def export_summary_with_error(exporter, summary, unwritable_file):
    with pytest.raises(ExportError) as error_info:
        exporter.export(summary)
    return error_info.value


@then("the file is written")
def check_file_written(exported_path):
    assert exported_path.is_file()


@then(parsers.parse('the file name is "{expected_name}"'))
def check_file_name(exported_path, expected_name):
    assert exported_path.name == expected_name


@then(parsers.parse('the file content starts with "{prefix}"'))
def check_file_content(exported_path, prefix):
    content = exported_path.read_text(encoding="utf-8")
    assert content.startswith(prefix)


@then(parsers.parse('the error message contains "{expected_message}"'))
def check_error_message(error, expected_message):
    assert expected_message in str(error)