# Synthetic BIDSified fixture

Run `python create_fixture.py` from this directory to regenerate `sample_bidsified/`.

The fixture contains one subject with two sessions. Each session has relative `dcm` and `raw` symlinks, two tiny DICOM instances, four acquisition sequences plus an RF-sensitivity acquisition, conversion output, and LORAKS output for two echoes, magnitude/phase parts, and one run.

The DICOM files contain a small explicit-VR dataset. The compressed NIfTI files are valid NIfTI-1 single-volume files with four float32 voxels. The `.dat` files are deliberately tiny synthetic Twix-shaped stand-ins: they preserve the repository's Siemens-style filenames and carry a small deterministic payload, but are not suitable input for the MATLAB LORAKS reconstruction.