# Run LORAKS Reconstruction

This page describes how to reconstruct the raw MRI data acquired in the IronSleep project to magnitude and phase maps in the NIfTI data format. 

The scripts that are described on this page are part of the **batch_LORAKSreco** repository ([Gitlab Repository](https://gitlab.gwdg.de/cbs-neurophy/batch_loraksreco), [Public Github repo](https://github.com/nkuegler/batch_LORAKSreco)). Feel free to clone or fork the repository. If you encounter any problems, [send me an e-mail](mailto:kuegler@cbs.mpg.de?subject=Problems%20with%20loraks_reconstruction) or a message on Minerva (user: kuegler).

---

## Table of Contents

1. [Usage](#usage)
    - [Necessary software (repositories)](#necessary-software-repositories)
    - [How to run the LORAKS reconstruction](#how-to-run-the-loraks-reconstruction)
2. [ToDos](#todos)

---

## Usage
The scripts in the **batch_LORAKSreco** repository are used to specify paths, configure the LORAKS reconstruction, and submit the reconstruction of each session's data in a separate batch job utilizing SLURM.<br>
If your data differs substantially from the data these scripts were designed for, you may need to adjust the code and configuration files accordingly.<br>
The logs are saved in separate directories in the `logs/` folder (excluded from the repository by adding it to the `.gitignore`). You can define the log file output path in the `recon.sh` script (see Step 6 below).

### Necessary software (repositories)
+ **image-reconstruction**
    + This [repository on the Neurophysics Gitlab](https://gitlab.gwdg.de/cbs-neurophy/image-reconstruction) contains the actual MATLAB implementation of the LORAKS reconstruction.
    + Make sure to use the the branch `WIP_romeoPhaseUnwrapping`, where you can use ROMEO for phase unwrapping during MCPC-3D-S coil combination instead of robustUnwrap. 
+ **CompileMRI (mritools including ROMEO)**
    + Information on how to install ROMEO and how to include it in the config file for the reconstruction can be found in the `WIP_romeoPhaseUnwrapping` branch's README under the heading *Using ROMEO for phase unwrapping during MCPC-3D-S coil combination*.
    + As stated in the **image_reconstruction** README, download the latest release of [ROMEO from Github](https://github.com/korbinian90/CompileMRI.jl/releases) (on MPI CBS computers, download the version compiled for Ubuntu 20.04).
    + Examples of the `loraksConfig.json` can be found in the **batch_LORAKSreco** repository.
+ **batch_LORAKSreco** 
    + This repository contains scripts to submit the reconstructions of all specified sessions as separate batch jobs to a compute server using SLURM. [Reach out](mailto:kuegler@cbs.mpg.de?subject=Problems%20with%20loraks_reconstruction) if you encounter problems or need help with the code (kuegler@cbs.mpg.de).

### How to run the LORAKS reconstruction
The python script `recon_call.py` inherits parameters specified in `config_ironsleep.py` (mainly paths and file names). According to those, it builds the commands for submitting jobs to the SLURM compute server.<br> 
You will only define a parent input directory, where the script will recursively process each subject and session folder that is specified in the `config_ironsleep.py` file. It is important, that the folder/file structure is conform with: 
```
parent_dir/
├── subject_01/
│   ├── session_01/
│   │   └── [raw data files]
│   ├── session_02/
│   │   └── [raw data files]
│   └── session_03/
│       └── [raw data files]
├── subject_02/
│   ├── session_01/
│   │   └── [raw data files]
│   └── session_02/
│       └── [raw data files]
└── subject_03/
    └── session_01/
        └── [raw data files]
```

The shell script `recon.sh` specifies the task and the required resources in the SBATCH notation (output of the logs is specified by `SBATCH -o /path/to/logs/dir/%j.out`). The *reconstruction* command uses the parameters specified in the `loraksConfig.json`, which must be adjusted to use the ROMEO phase unwrapping. 

+ **Step 0:**
    + Set up miniforge, so you can use the conda (or mamba) package manager (you can follow the instructions in [Setting up Conda](https://wiki.cbs.mpg.de/spaces/CBSNP/pages/158105663/Setting+up+Conda)).

+ **Step 1:**
    + Connect to a SLURM compute server *(only for MPI CBS compute infrastructure)*
    + ```
      getserver -sb
      ```

+ **Step 2:**
    + **Make sure** that you checked out the `WIP_romeoPhaseUnwrapping` branch in the local clone of the **image-reconstruction** repository. Otherwise the ROMEO phase unwrapping will not be used. 
    + ```
      cd /path/to/image-reconstruction
      git branch
      git checkout WIP_romeoPhaseUnwrapping     # if the asterisk * is not next to WIP_romeoPhaseUnwrapping
      ```

+ **Step 3:** 
    + Activate a virtual environment containing a recent python version. The Bidsme environment provided in the Bidsification step should be sufficient.
    + ```
      # conda env create -f environment.yml   # create environment from environment.yml if you have not done this yet
      conda activate env_name   # activate environment
      ```

+ **Step 4:**
    + Access the `config_ironsleep.py` file and define the following parameters:
        + `sub_ses`: nested list, defining subject name and one or multiple session names (string or list of strings)
            + `[[subj1, sess1], [subj2, sess1], ...]` → session names as string if only one session per subject
            + `[[subj1, [sess1, sess2, sess3, ...]], [subj2, [sess1, sess2, sess3, ...]], ...]` → session names as list of strings if multiple sessions per subject
    + `input_parent`: directory where the subject and session folders containing the raw data are located
    + `output_parent`: directory where the subject and session folders are located that the reconstructed files are stored in
    + `name_storage_dir`: name of the directory that is created in each session's folder to store the reconstructed data
    + `with_smaps`: reconstruct corresponding sensitivity maps for each raw data file 
        + If `with_smaps = True` in the config file, the number of sessions specified in `sub_ses` is considered double. Every raw data file name **MUST** be accompanied by an smap file in this case (either specified before or after the corresponding raw data file in the dictionaries described below)!
        + If there is no smap available or you don't want to reconstruct one for a specific session, you still need to add an empty string `""` or a `"placeholder"` string at the correct position. This will avoid submitting a batch job for this file (as no file matching this name can be found in the specified directory).
    + `pdw_raw`: nested list, defining the file names of the the separate PD-weighted raw MRI files
        + ```python
            [
            [file_sess1, file_sess2, file_sess3, ...], # for subj1
            [file_sess1, file_sess2, file_sess3, ...], # for subj2
            [file_sess1, file_sess2, file_sess3, ...] # for subj3
            ]
            ```
        + `pdw_raw=None`, if you don't want to reconstruct PD-weighted data.
    + `t1w_raw`: nested list, defining the file names of the the separate T1-weighted raw MRI files
        + *structure: see pdw_raw*
        + `t1w_raw=None`, if you don't want to reconstruct T1-weighted data.
    + `mtw_raw`: nested list, defining the file names of the the separate MT-weighted raw MRI files
        + *structure: see pdw_raw*
        + `mtw_raw=None`, if you don't want to reconstruct MT-weighted data.
    + `ernst_raw`: nested list, defining the file names of the the separate Ernst-angle acquisition raw MRI files 
        + *structure: see pdw_raw*
        + `ernst_raw=None`, if you don't want to reconstruct Ernst-angle data.
    > Hint: 
    > If the specified file name is empty `""`, no batch job will be submitted for this file. 

+ **Step 5:**
    + Create the correct `loraksConfig.json` according to the instructions in the README of the `WIP_romeoPhaseUnwrapping` branch in the **image-reconstruction** repository. Make sure that the `loraksConfig.json` is located in the same directory as the `recon.sh` script!
    + An example can be found in the **batch_LORAKSreco** repository but you need to adjust the `romeoBinaryPath` to the location of your ROMEO installation.
    + ```
      {
       "method": "loraks",
       "useNoiseMeasurements": false,
       "romeoBinaryPath": "/path/to/bin/romeo",
       "multiEchoPhaseUnwrappingMethod": "romeo"
      }
      ```
    > Warning: The reconstruction may fail for very small matrices as the `rank parameter can't be larger than the matrix dimensions`. I encountered this problem when trying to reconstruct sensitivity maps acquired with the body coil. To overcome the issue, you need to adjust the `rank` parameter in the config file `loraksConfig_adjRank.json`.

+ **Step 6:**
    + Access the `recon.sh` script and adjust the required resources and log file output path in the SBATCH parameters. The more resources you request for the job, the later your job will be scheduled. Try to keep the resource request as high as necessary, but as low as possible.
    + Also adjust the paths pointing to the `loraksConfig.json` and to the local clone of the **image-reconstruction** repository in the reconstruction command. 
    + The MATLAB version is specified as 9.16 but other versions may also work (not tested).
    + ```
      #SBATCH -c 16					# 16 cores for fast reco
      #SBATCH --mem 500G			# 0.5 mm fully sampled is around 220G, need maybe double
      #SBATCH --time 1800			# 10 echoes at 2 hours per echo but some nodes take 3 hours per echo
      #SBATCH -o /data/u_kuegler_software/git/batch_LORAKSreco/logs/ironsleep_TH/%j.out	# redirect the output to log files

      rawdata=$1
      outdir=$2

      echo "rawdata: $rawdata"
      echo "outdir: $outdir"

      MATLAB -v 9.16 matlab -batch "reconstruction('$rawdata','$outdir','/path/to/loraksConfig.json');exit" -sd /path/to/image-reconstruction
      ```

+ **Step 7:** 
    + Submit all the specified jobs to the SLURM compute server by running the `recon_call.py` script from the terminal.
        + Check that the correct config file is imported in `recon_call.py` (especially if you created a new config file with a different name).
    + Reminder: Make sure that you are on the SLURM compute server (Step 1) and that the correct conda environment is activated (Step 3).
    + ```
      cd /path/to/batch_LORAKSreco
      ./recon_call.py
      ````

+ **Step 8:**
    + Check if the batch jobs were submitted and are now running or pending using the commands `sacct` or `squeue -u $USER` (on the SLURM cluster).
    + More information on SLURM commands can be found [here](https://slurm.schedmd.com/quickstart.html).


> Additional information: 
> Running the `recon_call.py` script will save all individual paths to the raw data files that were specified for the LORAKS reconstruction to `output_parent/loraks_rawData_YYMMDD_HHMM.json`.


## ToDos:
+ try out, document, and commit how to use UV instead of conda
+ adjust all paths to Pathlib instead of OS or other path libraries, so that the application will also run on Windows computers. (Although additional changes may be needed for full Windows compatibility, this change improves cross-platform support.)
+ raw data filenames should rather be specified in a list with arbitrary number of files to account for non-standard acquisitions (drop the whole validity check based on number of files within `recon_call.py`)
+ default rank 150 does not work for all smaps (must be adjusted in loraksConfig.json) -> implement rank specification (or rather loraksConfig file specification) in config file
+ The json file saved to document which files were reconstructed does not seem to include all the smaps when `with_smaps=True` (seems to only include the first file of a session). Check and fix this.