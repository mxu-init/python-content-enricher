from unittest.mock import patch

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

import src.exporter as exporter_module
from src.exporter import ExportError, SummaryTextExporter
from src.summarizer import ArticleSummary

scenarios("features/exporter.feature")


@pytest.fixture
def output_directory(tmp_path):
    with patch.object(exporter_module, "OUTPUT_DIRECTORY", tmp_path):
        yield tmp_path


@pytest.fixture
def summary():
    return None


@given(
    parsers.parse('a summary titled "{title}" with the text "{text}"'),
    target_fixture="summary",
)
def summary_with_text(title, text):
    return ArticleSummary(title=title, text=text)


@when("the summary is exported", target_fixture="exported_file")
def export_summary(summary, output_directory):
    return SummaryTextExporter().export(summary)


@then(parsers.parse('a text file "{expected_name}" is created'))
def check_exported_file(exported_file, expected_name):
    assert exported_file.name == expected_name
    assert exported_file.is_file()


@then("the text file contains the title and the summary")
def check_text_file_content(exported_file, summary):
    content = exported_file.read_text(encoding="utf-8")
    assert f"Resumen: {summary.title}" in content
    assert summary.text in content


@when("the summary cannot be exported")
def export_fails(summary, monkeypatch):
    def raise_os_error(self, file_path, summary):
        raise OSError("Bloqueado por el sistema de archivos.")

    monkeypatch.setattr(SummaryTextExporter, "_write_file", raise_os_error)
    with pytest.raises(ExportError):
        SummaryTextExporter().export(summary)


@then("an export error is raised")
def check_export_error():
    pass
