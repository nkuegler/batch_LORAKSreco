#!/usr/bin/env python3

"""Command-line entry point for submitting configured LORAKS jobs."""

import json
import os
import subprocess
import warnings
from datetime import datetime
from types import ModuleType

from recon_helpers import validate_config, validate_raw_files


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RECON_SCRIPT = os.path.join(SCRIPT_DIR, "recon.sh")
SLURM_PARTITION = "standard,group_servers,gr_weiskopf"


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
    validate_raw_files(input_parent, sub_ses, raw_configs)
    for subject_index, (subject_name, sessions) in enumerate(sub_ses):
        if isinstance(sessions, str):
            sessions = [sessions]

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
