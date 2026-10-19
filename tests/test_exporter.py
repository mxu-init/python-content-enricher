from pathlib import Path
from unittest.mock import patch

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

import src.exporters as exporter_module
from src.exporters import BaseExporter, ExportError, PdfExporter, TxtExporter
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
    return TxtExporter().export_summary(summary)


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

    monkeypatch.setattr(TxtExporter, "_write_file", raise_os_error)
    with pytest.raises(ExportError):
        TxtExporter().export_summary(summary)


@then("an export error is raised")
def check_export_error():
    pass


def test_resolve_path_with_extension_and_custom_path(tmp_path):
    exporter = BaseExporter()
    custom_path = str(tmp_path / "custom.txt")
    resolved = exporter._resolve_path(custom_path, "txt")
    assert resolved == Path(custom_path)


def test_txt_exporter_export_success(tmp_path):
    exporter = TxtExporter()
    path = exporter.export(str(tmp_path / "test"), "Original", "Enriched", "Translated")
    assert path.is_file()
    content = path.read_text(encoding="utf-8")
    assert "Original" in content
    assert "Enriched" in content
    assert "Translated" in content


def test_txt_exporter_export_empty_filename():
    exporter = TxtExporter()
    with pytest.raises(ValueError):
        exporter.export("", "Original", "Enriched", "Translated")


def test_txt_exporter_export_os_error(monkeypatch, tmp_path):
    exporter = TxtExporter()
    monkeypatch.setattr("builtins.open", lambda *a, **kw: (_ for _ in ()).throw(OSError("Disk full")))
    with pytest.raises(IOError):
        exporter.export(str(tmp_path / "test"), "Original", "Enriched", "Translated")


def test_pdf_exporter_export_success(tmp_path):
    exporter = PdfExporter()
    path = exporter.export(str(tmp_path / "test"), "Original", "Enriched", "Translated")
    assert path.is_file()


def test_pdf_exporter_export_empty_filename():
    exporter = PdfExporter()
    with pytest.raises(ValueError):
        exporter.export("", "Original", "Enriched", "Translated")


def test_pdf_exporter_export_error(monkeypatch, tmp_path):
    exporter = PdfExporter()
    monkeypatch.setattr("src.exporters.SimpleDocTemplate", lambda *a, **kw: (_ for _ in ()).throw(RuntimeError("PDF error")))
    with pytest.raises(RuntimeError):
        exporter.export(str(tmp_path / "test"), "Original", "Enriched", "Translated")


def test_pdf_exporter_export_summary_success(tmp_path):
    exporter = PdfExporter()
    summary = ArticleSummary(title="Test", text="Summary text")
    path = exporter.export_summary(summary, str(tmp_path / "summary_test.pdf"))
    assert path.is_file()


def test_pdf_exporter_export_summary_error(monkeypatch, tmp_path):
    exporter = PdfExporter()
    summary = ArticleSummary(title="Test", text="Summary text")
    monkeypatch.setattr("src.exporters.SimpleDocTemplate", lambda *a, **kw: (_ for _ in ()).throw(Exception("PDF build failed")))
    with pytest.raises(ExportError):
        exporter.export_summary(summary, str(tmp_path / "summary_test.pdf"))
