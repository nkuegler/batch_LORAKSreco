"""Tests for reconstruction planning without submitting to SLURM.

`recon_call.sbatch_commands` receives a small config object and a fake submit
callable. This verifies path construction and bookkeeping while keeping CI
independent of a cluster and MATLAB installation.
"""

import json
from datetime import datetime
from types import SimpleNamespace

import pytest

from recon_call import sbatch_commands, validate_config
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


def test_sbatch_commands_builds_all_modality_paths_and_json_record(tmp_path):
    submitted = []
    output_parent = tmp_path / "output"
    config = make_config(SYNTHETIC_DATA, output_parent)

    sbatch_commands(config, submitted.append, datetime(2026, 9, 30, 12, 34))

    assert len(submitted) == 8
    assert all(command.startswith("sbatch -p standard") for command in submitted)
    assert all("/sub-SYNTH01/" in command for command in submitted)
    record = json.loads((output_parent / "loraks_rawData_20260930_1234.json").read_text())
    assert set(record["sub-SYNTH01"]) == {"ses-20260722", "ses-20260804"}
    assert set(record["sub-SYNTH01"]["ses-20260722"]) == {"t1w", "pdw", "mtw", "ernst"}


def test_existing_output_session_is_skipped(tmp_path):
    output_parent = tmp_path / "output"
    skipped = output_parent / "sub-SYNTH01" / "ses-20260722" / "nii_loraks_recon"
    skipped.mkdir(parents=True)
    (skipped / "already_exists.nii.gz").write_bytes(b"fixture")
    submitted = []

    with pytest.warns(UserWarning, match="is not empty"):
        sbatch_commands(make_config(SYNTHETIC_DATA, output_parent), submitted.append, datetime(2026, 9, 30, 12, 35))

    assert len(submitted) == 4
    record = json.loads((output_parent / "loraks_rawData_20260930_1235.json").read_text())
    assert "ses-20260722" not in record["sub-SYNTH01"]
    assert "ses-20260804" in record["sub-SYNTH01"]


def test_validate_config_expands_sensitivity_map_sessions():
    expanded = validate_config(
        [["sub", ["ses"]]], [["a", "b", "c"]], [["a", "b", "c"]],
        [["a", "b", "c"]], None, True, 2,
    )

    assert expanded == [["sub", ["ses", "ses", "ses"]]]


def test_validate_config_rejects_mismatched_raw_file_lists():
    with pytest.raises(ValueError, match="Length of pdw_raw"):
        validate_config([["sub", ["ses"]]], [["a"]], None, None, None, True, 2)


def test_validate_config_rejects_invalid_session_types():
    with pytest.raises(TypeError, match="Sessions must"):
        validate_config([["sub", 7]], None, None, None, None, False, 0)
