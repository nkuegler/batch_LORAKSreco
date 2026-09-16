#!/usr/bin/env python3

## subject names and session names
## if there are multiple sessions for a subject, the session names should be in a list
sub_ses = [["43472.ec", ["20250703_1", "20250703_2"]],
]

## directories of subjects and sessions for input and output
input_parent = "/data/p_03037/LORAKS_adults/source"
output_parent = "/data/p_03037/LORAKS_adults/source"
name_storage_dir = "nii_loraks_recon_extraMTw"   # name of the directory in the output_parent where the reconstructed data will be stored

with_smaps = False # boolean, specifies if sensitivity maps are also reconstructed
                   # each session file MUST have a corresponding sensitivity map file (2x length of t1w_raw, pdw_raw, mtw_raw)
                   # handled so that each specified session in sub_ses is used twice

## specifying names of the actual pdw, t1w, mtw, and ernst .dat files
## Each one has to be a nested list, where the sessions of each subject are specified in a separate list.
pdw_raw = None
           
t1w_raw = None

mtw_raw = [[  # 43472.ec 
              "meas_MID00107_FID142072_mtw_kp_mtflash3d_v1s_1p0_fa220.dat",        # 20250703_1
              "meas_MID00133_FID142098_mtw_kp_mtflash3d_v1s_1p0_fa220.dat",        # 20250703_2
           ]
]
ernst_raw = None

b1afi_ptx_raw = None

b1afi_stx_raw = None