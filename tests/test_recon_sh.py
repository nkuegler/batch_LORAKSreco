"""Shell-level tests for recon.sh configuration selection and exit status."""

import os
import stat
import subprocess
from pathlib import Path


SCRIPT = Path(__file__).parent.parent / "recon.sh"


def make_script_environment(tmp_path, matlab_status=0):
    script_dir = tmp_path / "script"
    script_dir.mkdir()
    script = script_dir / "recon.sh"
    script.write_bytes(SCRIPT.read_bytes())
    (script_dir / "loraksConfig.json").write_text("normal")
    (script_dir / "loraksConfig_adjRank.json").write_text("adjusted")

    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    matlab = bin_dir / "MATLAB"
    matlab.write_text(f"#!/bin/bash\nprintf '%s\\n' \"$@\" > \"$MATLAB_ARGS\"\nexit {matlab_status}\n")
    matlab.chmod(matlab.stat().st_mode | stat.S_IXUSR)
    return script, bin_dir


def run_recon(script, bin_dir, tmp_path, raw_name):
    args_file = tmp_path / "matlab_args.txt"
    environment = os.environ | {"PATH": f"{bin_dir}:{os.environ['PATH']}", "MATLAB_ARGS": str(args_file)}
    result = subprocess.run(
        ["bash", str(script), raw_name, str(tmp_path / "output"), str(script.parent)],
        env=environment,
        capture_output=True,
        text=True,
    )
    return result, args_file.read_text() if args_file.exists() else ""


def test_recon_sh_selects_adjusted_config_for_sensitivity_data(tmp_path):
    script, bin_dir = make_script_environment(tmp_path)
    result, matlab_args = run_recon(script, bin_dir, tmp_path, "meas_rfsens.dat")

    assert result.returncode == 0
    assert "loraksConfig_adjRank.json" in matlab_args


def test_recon_sh_selects_normal_config_for_regular_data(tmp_path):
    script, bin_dir = make_script_environment(tmp_path)
    result, matlab_args = run_recon(script, bin_dir, tmp_path, "meas_pdw.dat")

    assert result.returncode == 0
    argument_lines = matlab_args.splitlines()
    assert any("loraksConfig.json" in line and "adjRank" not in line for line in argument_lines)


def test_recon_sh_returns_matlab_failure(tmp_path):
    script, bin_dir = make_script_environment(tmp_path, matlab_status=23)
    result, _ = run_recon(script, bin_dir, tmp_path, "meas_pdw.dat")

    assert result.returncode == 23


def test_recon_sh_fails_before_matlab_when_config_is_missing(tmp_path):
    script, bin_dir = make_script_environment(tmp_path)
    (script.parent / "loraksConfig.json").unlink()
    (script.parent / "loraksConfig_adjRank.json").unlink()
    result, matlab_args = run_recon(script, bin_dir, tmp_path, "meas_pdw.dat")

    assert result.returncode == 1
    assert "Failed to find config" in result.stdout
    assert matlab_args == ""
