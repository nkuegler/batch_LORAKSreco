"""Contract tests for the small BIDSified fixture used by CI.

These tests intentionally validate structure and file signatures only. They do not
attempt to run MATLAB or interpret the synthetic raw-data payload as real Twix.
"""

import gzip
import struct
from pathlib import Path

from .conftest import SYNTHETIC_DATA


SESSIONS = ("ses-20260722", "ses-20260804")
SEQUENCES = ("t1w", "pdw", "mtw", "ernst")


def test_subject_has_two_sessions_with_expected_links_and_outputs():
    subject = SYNTHETIC_DATA / "sub-SYNTH01"
    assert sorted(path.name for path in subject.iterdir()) == list(SESSIONS)

    for session_name in SESSIONS:
        session = subject / session_name
        assert (session / "dcm").is_symlink()
        assert (session / "raw").is_symlink()
        assert (session / "dcm").is_dir()
        assert (session / "raw").is_dir()
        assert (session / "nii_loraks_recon").is_dir()

    assert (subject / SESSIONS[0] / "nii").is_dir()
    assert (subject / SESSIONS[1] / "nii_dcm2niix").is_dir()


def test_each_session_covers_acquisitions_echoes_parts_and_runs():
    subject = SYNTHETIC_DATA / "sub-SYNTH01"
    for session_name in SESSIONS:
        session = subject / session_name
        raw_names = [path.name for path in (session / "raw").glob("*.dat")]
        assert len(raw_names) == 5
        assert all(any(f"_{sequence}_" in name for name in raw_names) for sequence in SEQUENCES)
        assert any("_rfsens_" in name for name in raw_names)

        outputs = [path.name for path in (session / "nii_loraks_recon").glob("*.nii.gz")]
        assert len(outputs) == 16
        assert all(any(f"echo-{echo}" in name for name in outputs) for echo in ("01", "02"))
        assert all(any(f"part-{part}" in name for name in outputs) for part in ("mag", "phase"))
        assert all(any(f"acq-{sequence}" in name for name in outputs) for sequence in SEQUENCES)
        assert all("run-01" in name for name in outputs)


def test_dicom_and_nifti_files_have_minimal_valid_signatures():
    subject = SYNTHETIC_DATA / "sub-SYNTH01"
    for session_name in SESSIONS:
        session = subject / session_name
        dicom_files = list((session / "dcm").rglob("*.dcm"))
        assert len(dicom_files) == 2
        assert all(path.read_bytes()[128:132] == b"DICM" for path in dicom_files)

        nifti_files = list((session / "nii_loraks_recon").glob("*.nii.gz"))
        for path in nifti_files:
            with gzip.open(path, "rb") as input_file:
                header = input_file.read(352)
            assert struct.unpack_from("<i", header, 0)[0] == 348
            assert struct.unpack_from("<3h", header, 42) == (2, 2, 1)

        raw_files = list((session / "raw").glob("*.dat"))
        assert all(path.read_bytes().startswith(b"SYNTHETIC-TWIX\0") for path in raw_files)


def test_fixture_generator_is_idempotent(tmp_path):
    """A clean checkout can regenerate the fixture without symlink collisions."""
    import importlib.util

    source = Path(__file__).parent / "synthetic_testdata" / "create_fixture.py"
    spec = importlib.util.spec_from_file_location("create_fixture", source)
    generator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(generator)
    generator.ROOT = tmp_path / "sample_bidsified"

    generator.main()
    generator.main()

    assert len(list(generator.ROOT.rglob("*.dcm"))) == 4
    assert len(list(generator.ROOT.rglob("*.dat"))) == 10
    assert len(list(generator.ROOT.rglob("*.nii.gz"))) == 40
