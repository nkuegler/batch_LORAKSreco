# Automated tests

The test suite is intentionally divided by responsibility so failures point to a small part of the workflow.

| Module | Protects | External tools |
| --- | --- | --- |
| `test_synthetic_fixture.py` | Subject/session layout, symlinks, acquisition coverage, DICOM/NIfTI/raw signatures, and fixture regeneration | None |
| `test_config_template.py` | Placeholder counts, sensitivity-map variants, and generated Python syntax | None |
| `test_recon_call.py` | Session expansion, raw path construction, skip behavior, SLURM command creation, and JSON bookkeeping | Fake submit callback |
| `test_recon_sh.py` | Sensitivity config selection, normal config selection, missing-config failure, and MATLAB exit-code propagation | Fake `MATLAB` executable |

Run all tests from the repository root:

```bash
python -m pytest -q
```

The synthetic `.dat` files are deliberately small stand-ins and are not passed to MATLAB. The shell tests verify wrapper behavior with a fake executable instead. A future MATLAB integration job should be separate from this fast push-time suite.
