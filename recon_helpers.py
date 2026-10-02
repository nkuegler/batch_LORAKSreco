#!/usr/bin/env python3

"""Reusable configuration validation and SLURM submission helpers."""

import os


def _sessions(sub_ses, with_smaps, smaps_per_session):
    if with_smaps:
        return [
            [subject, [session for item in ([sessions] if isinstance(sessions, str) else sessions)
                       for session in [item] * (smaps_per_session + 1)]]
            for subject, sessions in sub_ses
        ]
    return sub_ses


def validate_config(sub_ses, pdw_raw, t1w_raw, mtw_raw, ernst_raw, with_smaps, smaps_per_session):
    """Validate configuration nesting, session types, and raw-file list lengths."""
    if not isinstance(sub_ses, list):
        raise TypeError("sub_ses must be a list")

    for subject_entry in sub_ses:
        if not isinstance(subject_entry, (list, tuple)) or len(subject_entry) != 2:
            raise TypeError("Each sub_ses entry must contain a subject and sessions")
        subject_name, sessions = subject_entry
        if not isinstance(subject_name, str) or not subject_name:
            raise TypeError("Subject names must be non-empty strings")
        if isinstance(sessions, str):
            if not sessions:
                raise TypeError("Session names must be non-empty strings")
        elif isinstance(sessions, list):
            if not sessions or not all(isinstance(session, str) and session for session in sessions):
                raise TypeError("Sessions must be a non-empty list of non-empty strings")
        else:
            raise TypeError(f"Sessions must be of type list or string, got {type(sessions).__name__}")

    expanded_sub_ses = _sessions(sub_ses, with_smaps, smaps_per_session)
    expected_sessions_per_subject = []
    for _, sessions in expanded_sub_ses:
        if isinstance(sessions, str):
            session_count = 1
        elif isinstance(sessions, list):
            session_count = len(sessions)
        else:
            raise TypeError(f"Sessions must be of type list or string, got {type(sessions).__name__}")
        expected_sessions_per_subject.append(session_count)

    for name, raw_files in (("pdw_raw", pdw_raw), ("t1w_raw", t1w_raw),
                            ("mtw_raw", mtw_raw), ("ernst_raw", ernst_raw)):
        if raw_files is None:
            continue
        if not isinstance(raw_files, list) or len(raw_files) != len(expanded_sub_ses):
            raise ValueError(f"{name} must contain one list for each subject")
        for subject_index, entries in enumerate(raw_files):
            if not isinstance(entries, list) or len(entries) != expected_sessions_per_subject[subject_index]:
                raise ValueError(f"Length of {name} must be the same as the number of sessions")
            if not all(isinstance(filename, str) for filename in entries):
                raise TypeError(f"Entries in {name} must be strings")
    return expanded_sub_ses


def validate_raw_files(input_parent, sub_ses, raw_configs):
    """Raise an error for a configured non-empty raw filename that is missing."""
    for subject_index, (subject_name, sessions) in enumerate(sub_ses):
        if isinstance(sessions, str):
            sessions = [sessions]
        for session_index, session in enumerate(sessions):
            raw_dir = os.path.join(input_parent, subject_name, session, "raw")
            for modality, raw_files in raw_configs:
                if not raw_files:
                    continue
                filename = raw_files[subject_index][session_index]
                if filename and not os.path.isfile(os.path.join(raw_dir, filename)):
                    raise FileNotFoundError(
                        f"Configured {modality} raw file does not exist: "
                        f"{os.path.join(raw_dir, filename)}"
                    )
