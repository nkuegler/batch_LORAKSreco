#!/usr/bin/env python3

"""
This script is used to submit reconstruction jobs to a computing cluster using SLURM. 
It reads configuration variables from config.py, constructs input and output paths, and submits jobs 
for each subject and session specified in the configuration.
Functions:
    sbatch_commands: Submits jobs to the cluster for each subject and session.
    This function iterates over the subjects and sessions specified in the configuration,
    constructs the necessary input and output paths, and submits SLURM jobs for T1-weighted,
    PD-weighted, and MT-weighted raw data reconstruction.
    Raises:
        TypeError: If the subject name is not a string or if the session name is not a string or list.
"""


import os
import warnings
import json
from datetime import datetime

import default_configs.example_config as config # import the correct config file
import utils

# script defining slurm parameters and reconstruction command
script_dir = os.path.dirname(os.path.abspath(__file__))
recon_script = os.path.join(script_dir, 'recon.sh')

# configuration variables
input_parent = config.input_parent
output_parent = config.output_parent
t1w_raw = config.t1w_raw
pdw_raw = config.pdw_raw
mtw_raw = config.mtw_raw
ernst_raw = config.ernst_raw
sub_ses = config.sub_ses
name_storage_dir = config.name_storage_dir
smaps_per_session = config.smaps_per_session
enforce_same_session_length = config.enforce_same_session_length

## check if input_parent and output_parent exist
if not os.path.exists(input_parent):
    raise FileNotFoundError(f"Input parent directory {input_parent} does not exist")

if not os.path.exists(output_parent):
    print(f"Output parent directory {output_parent} does not exist. Creating it now.")
    os.makedirs(output_parent, exist_ok=True)

## define which data to reconstruct
t1w_recon = bool(t1w_raw)
pdw_recon = bool(pdw_raw)
mtw_recon = bool(mtw_raw)
ernst_recon = bool(ernst_raw)

# check if sub_ses, t1w, pdw, and mtw are of the same length
number_of_sessions = 0
for _, sessions in sub_ses:
    if isinstance(sessions, list):
        number_of_sessions += len(sessions)
    elif isinstance(sessions, str):
        number_of_sessions += 1
    else:
        raise TypeError(f"Sessions must be of type list or string, got {type(sessions).__name__}")

if pdw_recon and sum(len(sl) for sl in pdw_raw) != number_of_sessions:
    raise ValueError("Length of pdw_raw must be the same as the number of sessions")
if t1w_recon and sum(len(sl) for sl in t1w_raw) != number_of_sessions:
    raise ValueError("Length of t1w_raw must be the same as the number of sessions")
if mtw_recon and sum(len(sl) for sl in mtw_raw) != number_of_sessions:
    raise ValueError("Length of mtw_raw must be the same as the number of sessions")
if ernst_recon and sum(len(sl) for sl in ernst_raw) != number_of_sessions:
    raise ValueError("Length of ernst_raw must be the same as the number of sessions")

longest_session = None
# checks if nested list structure is valid
# finds longest session
for data in [t1w_raw,pdw_raw,mtw_raw,ernst_raw]:
        if data:
            utils.is_raw_valid(data,enforce_same_session_length)
            if not enforce_same_session_length:
                longest_session = utils.count_longest_session(data)
if enforce_same_session_length:
    longest_session = utils.count_longest_session(t1w_raw)

def sbatch_commands():
    output_paths_raw = {}  # store paths to the raw data for each subject and session -> export as json at the end of the script

    """
    Submit jobs to the cluster
    """
    for i, (subject_name, session_name) in enumerate(sub_ses):

        if not isinstance(subject_name, str):
            raise TypeError("Subject (sub_ses[0]) must be of type string")

        if isinstance(session_name, str):
            session_name = [session_name] # convert session element to list for iteration
        
        if isinstance(session_name, list):
            for j, sess in enumerate(session_name):
                
                # specify output directory (reconstructed data)
                output_dir = os.path.join(output_parent, subject_name, sess, name_storage_dir)
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir, exist_ok=True)
                
                if any(os.path.isfile(os.path.join(output_dir, f)) for f in os.listdir(output_dir)):
                    warnings.warn(f"Output path {output_dir} is not empty. Skipping this session.")
                    continue
                
                # specify input directory (raw data)
                input_path = os.path.join(input_parent, subject_name, sess, "raw")
                session_data = {}

                for k in range(longest_session):
                    if t1w_recon:
                        if len(t1w_raw[i][j]) > k and t1w_raw[i][j][k]:
                            t1w_input_path = os.path.join(input_path, t1w_raw[i][j][k])
                            os.system(f'sbatch -p standard,group_servers,gr_weiskopf {recon_script} {t1w_input_path} {output_dir} {script_dir}')
                            session_data['t1w'] = t1w_input_path
                        else:
                            pass # no batch job submitted

                    if pdw_recon:
                        if len(pdw_raw[i][j]) > k and pdw_raw[i][j][k]:
                            pdw_input_path = os.path.join(input_path, pdw_raw[i][j][k])
                            os.system(f'sbatch -p standard,group_servers,gr_weiskopf {recon_script} {pdw_input_path} {output_dir} {script_dir}')
                            session_data['pdw'] = pdw_input_path
                        else:
                            pass # no batch job submitted

                    if mtw_recon:
                        if len(mtw_raw[i][j]) > k and mtw_raw[i][j][k]:
                            mtw_input_path = os.path.join(input_path, mtw_raw[i][j][k])
                            os.system(f'sbatch -p standard,group_servers,gr_weiskopf {recon_script} {mtw_input_path} {output_dir} {script_dir}')
                            session_data['mtw'] = mtw_input_path
                        else: 
                            pass # no batch job submitted

                    if ernst_recon:
                        if len(ernst_raw[i][j]) > k and ernst_raw[i][j][k]:
                            ernst_input_path = os.path.join(input_path, ernst_raw[i][j][k])
                            os.system(f'sbatch -p standard,group_servers,gr_weiskopf {recon_script} {ernst_input_path} {output_dir} {script_dir}')
                            session_data['ernst'] = ernst_input_path
                        else:
                            pass # no batch job submitted
                
                # store paths to the raw data for each subject and session
                if subject_name not in output_paths_raw:
                    output_paths_raw[subject_name] = {}
                output_paths_raw[subject_name][sess] = session_data

        else:
            raise TypeError("Session (sub_ses[1]) must be of type string or list")

    
    # export paths that were used for reconstruction for documentation purposes
    current_time = datetime.now().strftime("%Y%m%d_%H%M")
    output_filename = f'loraks_rawData_{current_time}.json'
    with open(os.path.join(output_parent, output_filename), 'w') as json_file:
        json.dump(output_paths_raw, json_file, indent=4)



if __name__ == "__main__":
    sbatch_commands()
