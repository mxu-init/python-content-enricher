import pytest
from pathlib import Path
from pytest_bdd import given, parsers, scenarios, then, when

from src.exporters import TxtExporter, PdfExporter

scenarios("features/exporters.feature")


@pytest.fixture
def export_context():
    return {}


@given(parsers.parse('a file name "{filename}" and format "{fmt}"'))
def setup_export_data(export_context, filename, fmt):
    export_context["filename"] = filename
    export_context["format"] = fmt
    export_context["original"] = "Texto original de prueba"
    export_context["enriched"] = "Texto enriquecido con IA"
    export_context["translated"] = "Translated content"


@when("the exporter saves the content")
def save_content(tmp_path, export_context):
    file_path = tmp_path / export_context["filename"]
    export_context["temp_path"] = file_path
    
    if export_context["format"] == "txt":
        exporter = TxtExporter()
        exporter.export(
            str(file_path),
            export_context["original"],
            export_context["enriched"],
            export_context["translated"]
        )
    elif export_context["format"] == "pdf":
        exporter = PdfExporter()
        exporter.export(
            str(file_path),
            export_context["original"],
            export_context["enriched"],
            export_context["translated"]
        )


@then(parsers.parse('the file "{expected_name}" should be created successfully'))
def verify_file_created(tmp_path, expected_name):
    final_file = tmp_path / expected_name
    assert final_file.exists()
    assert final_file.stat().st_size > 0