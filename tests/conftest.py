"""Shared paths and helpers for the fast, external-tool-free test suite."""

import importlib.util
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).parent.parent
SYNTHETIC_DATA = REPOSITORY_ROOT / "tests" / "synthetic_testdata" / "sample_bidsified"


def _ensure_synthetic_data():
	"""Generate the ignored fixture when running from a clean checkout."""
	if SYNTHETIC_DATA.exists():
		return

	generator_path = SYNTHETIC_DATA.parent / "create_fixture.py"
	spec = importlib.util.spec_from_file_location("synthetic_fixture_generator", generator_path)
	if spec is None or spec.loader is None:
		raise RuntimeError(f"Could not load synthetic fixture generator: {generator_path}")
	generator = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(generator)
	generator.main()


_ensure_synthetic_data()
