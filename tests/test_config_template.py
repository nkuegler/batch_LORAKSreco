"""Tests for generated reconstruction configuration structure."""

import py_compile

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
