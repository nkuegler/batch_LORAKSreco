"""Tests for reconstruction planning without submitting to SLURM.

`recon_call.sbatch_commands` receives a small config object and a fake submit
callable. This verifies path construction and bookkeeping while keeping CI
independent of a cluster and MATLAB installation.
"""

import json
from datetime import datetime
from types import SimpleNamespace

import pytest

from recon_call import SLURM_PARTITION, sbatch_commands
from recon_helpers import validate_config
from .conftest import SYNTHETIC_DATA


RAW_FILES = {
    "t1w": [
        "meas_MID001_t1w_kp_mtflash3d_synthetic.dat",
        "meas_MID002_t1w_kp_mtflash3d_synthetic.dat",
    ],
    "pdw": [
        "meas_MID001_pdw_kp_mtflash3d_synthetic.dat",
        "meas_MID002_pdw_kp_mtflash3d_synthetic.dat",
    ],
    "mtw": [
        "meas_MID001_mtw_kp_mtflash3d_synthetic.dat",
        "meas_MID002_mtw_kp_mtflash3d_synthetic.dat",
    ],
    "ernst": [
        "meas_MID001_ernst_kp_mtflash3d_synthetic.dat",
        "meas_MID002_ernst_kp_mtflash3d_synthetic.dat",
    ],
}


def make_config(input_parent, output_parent):
    return SimpleNamespace(
        input_parent=str(input_parent),
        output_parent=str(output_parent),
        name_storage_dir="nii_loraks_recon",
        sub_ses=[["sub-SYNTH01", ["ses-20260722", "ses-20260804"]]],
        with_smaps=False,
        smaps_per_session=2,
        pdw_raw=[RAW_FILES["pdw"]],
        t1w_raw=[RAW_FILES["t1w"]],
        mtw_raw=[RAW_FILES["mtw"]],
        ernst_raw=[RAW_FILES["ernst"]],
    )


def record_submission(submitted):
    def submit(command, check):
        assert check is True
        submitted.append(command)

    return submit


def test_sbatch_commands_builds_all_modality_paths_and_json_record(tmp_path):
    submitted = []
    output_parent = tmp_path / "output"
    config = make_config(SYNTHETIC_DATA, output_parent)

    sbatch_commands(config, record_submission(submitted), datetime(2026, 9, 30, 12, 34, 56))

    assert len(submitted) == 8
    assert all(command[:3] == ["sbatch", "-p", SLURM_PARTITION] for command in submitted)
    assert all("/sub-SYNTH01/" in command[4] for command in submitted)
    record = json.loads((output_parent / "loraks_rawData_20260930_123456.json").read_text())
    assert set(record["sub-SYNTH01"]) == {"ses-20260722", "ses-20260804"}
    assert set(record["sub-SYNTH01"]["ses-20260722"]) == {"t1w", "pdw", "mtw", "ernst"}


def test_existing_output_session_is_skipped(tmp_path):
    output_parent = tmp_path / "output"
    skipped = output_parent / "sub-SYNTH01" / "ses-20260722" / "nii_loraks_recon"
    skipped.mkdir(parents=True)
    (skipped / "already_exists.nii.gz").write_bytes(b"fixture")
    submitted = []

    with pytest.warns(UserWarning, match="is not empty"):
        sbatch_commands(make_config(SYNTHETIC_DATA, output_parent), record_submission(submitted), datetime(2026, 9, 30, 12, 35, 7))

    assert len(submitted) == 4
    record = json.loads((output_parent / "loraks_rawData_20260930_123507.json").read_text())
    assert "ses-20260722" not in record["sub-SYNTH01"]
    assert "ses-20260804" in record["sub-SYNTH01"]


def test_validate_config_expands_sensitivity_map_sessions():
    expanded = validate_config(
        [["sub", ["ses"]]], [["a", "b", "c"]], [["a", "b", "c"]],
        [["a", "b", "c"]], None, True, 2,
    )

    assert expanded == [["sub", ["ses", "ses", "ses"]]]


def test_validate_config_expands_scalar_session_names():
    expanded = validate_config(
        [["sub", "ses"]], [["a", "b", "c"]], None, None, None, True, 2,
    )

    assert expanded == [["sub", ["ses", "ses", "ses"]]]


def test_validate_config_rejects_mismatched_raw_file_lists():
    with pytest.raises(ValueError, match="Length of pdw_raw"):
        validate_config([["sub", ["ses"]]], [["a"]], None, None, None, True, 2)


def test_validate_config_rejects_invalid_session_types():
    with pytest.raises(TypeError, match="Sessions must"):
        validate_config([["sub", 7]], None, None, None, None, False, 0)


def test_validate_config_rejects_malformed_subject_entries():
    with pytest.raises(TypeError, match="Each sub_ses entry"):
        validate_config([["sub"]], None, None, None, None, False, 0)


def test_validate_config_rejects_malformed_modality_nesting():
    with pytest.raises(ValueError, match="one list for each subject"):
        validate_config([["sub", ["ses"]]], [["raw"], ["extra"]], None, None, None, False, 0)


def test_sbatch_commands_rejects_missing_configured_raw_file(tmp_path):
    config = make_config(tmp_path, tmp_path / "output")
    submitted = []

    with pytest.raises(FileNotFoundError, match="Configured t1w raw file does not exist"):
        sbatch_commands(config, record_submission(submitted), datetime(2026, 9, 30, 12, 36))

    assert submitted == []
