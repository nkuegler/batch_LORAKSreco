#!/usr/bin/env python3


"""Build and submit one reconstruction job per configured raw acquisition to a SLURM cluster. The script reads configuration variables from the specified config file (config_module)."""

import json
import os
import subprocess
import warnings
from datetime import datetime
from types import ModuleType


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RECON_SCRIPT = os.path.join(SCRIPT_DIR, "recon.sh")
SLURM_PARTITION = "standard,group_servers,gr_weiskopf"


def _sessions(sub_ses, with_smaps, smaps_per_session):
    if with_smaps:
        return [
            [subject, [session for item in sessions for session in [item] * (smaps_per_session + 1)]]
            for subject, sessions in sub_ses
        ]
    return sub_ses


def validate_config(sub_ses, pdw_raw, t1w_raw, mtw_raw, ernst_raw, with_smaps, smaps_per_session):
    """Validate session types and raw-file list lengths before submission."""
    expanded_sub_ses = _sessions(sub_ses, with_smaps, smaps_per_session)
    number_of_sessions = 0
    for _, sessions in expanded_sub_ses:
        if isinstance(sessions, str):
            number_of_sessions += 1
        elif isinstance(sessions, list):
            number_of_sessions += len(sessions)
        else:
            raise TypeError(f"Sessions must be of type list or string, got {type(sessions).__name__}")

    for name, raw_files in (("pdw_raw", pdw_raw), ("t1w_raw", t1w_raw),
                            ("mtw_raw", mtw_raw), ("ernst_raw", ernst_raw)):
        if raw_files and sum(len(entries) for entries in raw_files) != number_of_sessions:
            raise ValueError(f"Length of {name} must be the same as the number of sessions")
    return expanded_sub_ses


def sbatch_commands(config_module: ModuleType | None = None, submit=subprocess.run, now=None):
    """Submit configured jobs and write a JSON record of the raw paths used."""
    if config_module is None:
        import default_configs.config_histopark_20260928 as config_module

    input_parent = config_module.input_parent
    output_parent = config_module.output_parent
    pdw_raw = config_module.pdw_raw
    t1w_raw = config_module.t1w_raw
    mtw_raw = config_module.mtw_raw
    ernst_raw = config_module.ernst_raw
    with_smaps = config_module.with_smaps
    smaps_per_session = config_module.smaps_per_session
    sub_ses = validate_config(
        config_module.sub_ses, pdw_raw, t1w_raw, mtw_raw, ernst_raw,
        with_smaps, smaps_per_session,
    )

    if not os.path.exists(input_parent):
        raise FileNotFoundError(f"Input parent directory {input_parent} does not exist")
    os.makedirs(output_parent, exist_ok=True)

    output_paths_raw = {}
    raw_configs = (("t1w", t1w_raw), ("pdw", pdw_raw), ("mtw", mtw_raw), ("ernst", ernst_raw))
    for subject_index, (subject_name, sessions) in enumerate(sub_ses):
        if not isinstance(subject_name, str):
            raise TypeError("Subject (sub_ses[0]) must be of type string")
        if isinstance(sessions, str):
            sessions = [sessions]
        elif not isinstance(sessions, list):
            raise TypeError("Session (sub_ses[1]) must be of type string or list")

        for session_index, session in enumerate(sessions):
            output_dir = os.path.join(output_parent, subject_name, session, config_module.name_storage_dir)
            os.makedirs(output_dir, exist_ok=True)
            if any(os.path.isfile(os.path.join(output_dir, filename)) for filename in os.listdir(output_dir)):
                warnings.warn(f"Output path {output_dir} is not empty. Skipping this session.")
                continue

            input_path = os.path.join(input_parent, subject_name, session, "raw")
            session_data = {}
            for modality, raw_files in raw_configs:
                if not raw_files or not raw_files[subject_index][session_index]:
                    continue
                raw_path = os.path.join(input_path, raw_files[subject_index][session_index])
                submit(
                    [
                        "sbatch",
                        "-p",
                        SLURM_PARTITION,
                        RECON_SCRIPT,
                        raw_path,
                        output_dir,
                        SCRIPT_DIR,
                    ],
                    check=True,
                )
                session_data[modality] = raw_path

            output_paths_raw.setdefault(subject_name, {})[session] = session_data

    timestamp = (now or datetime.now()).strftime("%Y%m%d_%H%M")
    with open(os.path.join(output_parent, f"loraks_rawData_{timestamp}.json"), "w") as output_file:
        json.dump(output_paths_raw, output_file, indent=4)


if __name__ == "__main__":
    sbatch_commands()
