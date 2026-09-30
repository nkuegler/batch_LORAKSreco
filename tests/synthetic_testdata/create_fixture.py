#!/usr/bin/env python3

import gzip
import struct
from pathlib import Path


ROOT = Path(__file__).parent / "sample_bidsified"
SUBJECT = "sub-SYNTH01"
SESSIONS = ("ses-20260722", "ses-20260804")
SEQUENCES = ("t1w", "pdw", "mtw", "ernst")


def write_dicom(path: Path, session: str, instance: int) -> None:
    text = {
        (0x0008, 0x0016): "1.2.840.10008.5.1.4.1.1.4",
        (0x0008, 0x0018): f"1.2.826.0.1.3680043.10.543.{instance}",
        (0x0008, 0x0060): "MR",
        (0x0008, 0x103e): f"Synthetic {session}",
        (0x0010, 0x0010): "SYNTHETIC^SUBJECT",
        (0x0010, 0x0020): SUBJECT,
        (0x0020, 0x000d): "1.2.826.0.1.3680043.10.543.1",
        (0x0020, 0x000e): f"1.2.826.0.1.3680043.10.543.{instance + 100}",
    }
    elements = bytearray()
    for (group, element), value in text.items():
        encoded = value.encode("ascii") + (b" " if len(value) % 2 else b"")
        elements += struct.pack("<HH", group, element)
        elements += b"LO" if len(encoded) <= 0xFFFF else b"UT"
        elements += struct.pack("<H", len(encoded)) + encoded

    file_meta = bytearray()
    transfer_syntax = b"1.2.840.10008.1.2.1\0"
    file_meta += struct.pack("<HH2sH", 0x0002, 0x0001, b"OB", 2) + b"\0\1"
    file_meta += struct.pack("<HH2sH", 0x0002, 0x0002, b"UI", 26) + b"1.2.840.10008.5.1.4.1.1.4\0"
    file_meta += struct.pack("<HH2sH", 0x0002, 0x0010, b"UI", len(transfer_syntax)) + transfer_syntax
    group_length = struct.pack("<HH2sH", 0x0002, 0x0000, b"UL", 4) + struct.pack("<I", len(file_meta))
    path.write_bytes(b"\0" * 128 + b"DICM" + group_length + file_meta + elements)


def write_nifti(path: Path, value: float) -> None:
    header = bytearray(348)
    struct.pack_into("<i", header, 0, 348)
    struct.pack_into("<8h", header, 40, 3, 2, 2, 1, 1, 1, 1, 1)
    struct.pack_into("<h", header, 70, 16)
    struct.pack_into("<h", header, 72, 32)
    struct.pack_into("<8f", header, 76, 0, 1, 1, 1, 1, 1, 1, 1)
    struct.pack_into("<f", header, 108, 352)
    struct.pack_into("<f", header, 112, 1)
    header[123] = 10
    header[344:348] = b"n+1\0"
    payload = struct.pack("<4f", value, value + 1, value + 2, value + 3)
    with gzip.open(path, "wb") as output:
        output.write(header + b"\0" * 4 + payload)


def write_twix(path: Path, sequence: str, session: str) -> None:
    payload = (
        b"SYNTHETIC-TWIX\0"
        + f"sequence={sequence};session={session};samples=4;coils=1\n".encode("ascii")
        + struct.pack("<8f", 1.0, 0.0, 0.5, 0.5, 0.25, 0.25, 0.0, 0.0)
    )
    path.write_bytes(payload)


def main() -> None:
    shared = ROOT / "_shared"
    for session_index, session in enumerate(SESSIONS, start=1):
        dcm_dir = shared / "dcm" / session / "S10_synthetic_mtflash3d"
        raw_dir = shared / "raw" / session
        dcm_dir.mkdir(parents=True, exist_ok=True)
        raw_dir.mkdir(parents=True, exist_ok=True)
        for instance in range(1, 3):
            write_dicom(dcm_dir / f"synthetic_{session}_slice-{instance:02d}.dcm", session, session_index * 10 + instance)
        for sequence in SEQUENCES:
            write_twix(raw_dir / f"meas_MID{session_index:03d}_{sequence}_kp_mtflash3d_synthetic.dat", sequence, session)
        write_twix(raw_dir / f"meas_MID{session_index:03d}_rfsens_kp_mtflash3d_synthetic.dat", "rfsens", session)

        session_dir = ROOT / SUBJECT / session
        (session_dir / "nii_loraks_recon").mkdir(parents=True, exist_ok=True)
        conversion_dir = session_dir / ("nii" if session_index == 1 else "nii_dcm2niix")
        conversion_dir.mkdir(parents=True, exist_ok=True)
        for sequence_index, sequence in enumerate(SEQUENCES, start=1):
            write_nifti(conversion_dir / f"{SUBJECT}_{session}_{sequence}_run-01.nii.gz", sequence_index)
            for echo in ("01", "02"):
                for part, offset in (("mag", 0.0), ("phase", 0.25)):
                    name = f"{SUBJECT}_{session}_acq-{sequence}_echo-{echo}_part-{part}_run-01_desc-loraks.nii.gz"
                    write_nifti(session_dir / "nii_loraks_recon" / name, sequence_index + float(echo) + offset)

        dcm_link = session_dir / "dcm"
        raw_link = session_dir / "raw"
        dcm_link.unlink(missing_ok=True)
        raw_link.unlink(missing_ok=True)
        dcm_link.symlink_to(Path("../../_shared/dcm") / session)
        raw_link.symlink_to(Path("../../_shared/raw") / session)


if __name__ == "__main__":
    main()