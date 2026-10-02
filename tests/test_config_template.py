"""Tests for generated reconstruction configuration structure."""

import py_compile
import importlib
from uuid import uuid4

generator_module = importlib.import_module("generate_config_template")
from generate_config_template import generate_config_template, write_config_to_file


SUBJECTS = [["sub-a", ["ses-1", "ses-2"]], ["sub-b", ["ses-3"]]]


def test_template_has_one_raw_entry_group_per_session():
    config = generate_config_template(SUBJECTS, with_smaps=True, smaps_per_session=2)

    assert config["sub_ses"] == SUBJECTS
    assert len(config["pdw_raw"]) == 3
    assert all(len(entries) == 3 for entries in config["t1w_raw"])
    assert all(entries == ['""', '""', '""'] for entries in config["mtw_raw"])
    assert all(entries == ['""', '""', '""'] for entries in config["ernst_raw"])


def test_template_without_smaps_has_one_placeholder_per_session():
    config = generate_config_template(SUBJECTS, with_smaps=False)

    assert len(config["pdw_raw"]) == 3
    assert all(entries == ['""'] for entries in config["pdw_raw"])


def test_written_template_is_valid_python(tmp_path):
    output = tmp_path / "config_template.py"
    write_config_to_file(generate_config_template(SUBJECTS), output)

    py_compile.compile(str(output), doraise=True)
    contents = output.read_text()
    assert "sub-a" in contents
    assert "ses-2" in contents
    assert "pdw_raw =" in contents


def test_main_uses_configured_output_filename(tmp_path, monkeypatch):
    output = tmp_path / "custom_config.py"
    monkeypatch.setattr(generator_module, "output_filename", str(output))

    monkeypatch.chdir(tmp_path)
    generator_module.main()

    py_compile.compile(str(output), doraise=True)


def test_main_writes_default_output_relative_to_script(tmp_path, monkeypatch):
    filename = f"test_generated_config_{uuid4().hex}.py"
    monkeypatch.setattr(generator_module, "output_filename", filename)
    monkeypatch.chdir(tmp_path)

    expected = generator_module.Path(__file__).parent.parent / "default_configs" / "intermediate" / "generated_config.py"
    expected = expected.with_name(filename)
    try:
        generator_module.main()
        assert expected.is_file()
    finally:
        expected.unlink(missing_ok=True)
