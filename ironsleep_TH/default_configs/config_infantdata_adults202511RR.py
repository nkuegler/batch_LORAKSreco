#!/usr/bin/env python3

## subject names and session names
## if there are multiple sessions for a subject, the session names should be in a list
sub_ses = [["42577.9a", ["20250902_1"]],
]

## directories of subjects and sessions for input and output
input_parent = "/data/p_03037/LORAKS_adults/source"
output_parent = "/data/p_03037/LORAKS_adults/source"
name_storage_dir = "nii_loraks_recon"   # name of the directory in the output_parent where the reconstructed data will be stored

with_smaps = False # boolean, specifies if sensitivity maps are also reconstructed
                   # each session file MUST have a corresponding sensitivity map file (2x length of t1w_raw, pdw_raw, mtw_raw)
                   # handled so that each specified session in sub_ses is used twice
smaps_per_session = 0 # integer, number of sensitivity maps per session

## specifying names of the actual pdw, t1w, mtw, and ernst .dat files
## Each one has to be a nested list, where the sessions of each subject are specified in a separate list.
pdw_raw = [[   # 42577.9a
               "meas_MeasUID3000016_pdw_kp_mtflash3d_v1s_1p0_RR_250902_102716.dat",     # 20250902_1
           ],
]

t1w_raw = [[  # 42577.9a
               "meas_MeasUID3000014_t1w_kp_mtflash3d_v1s_1p0_RR_250902_102716.dat",     # 20250902_1
           ],
] 

mtw_raw = [[   # 42577.9a
               "meas_MeasUID3000018_mtw_kp_mtflash3d_v1s_1p0_FA180_RR_250902_102716.dat",     # 20250902_1
           ],
          ]

ernst_raw = None

b1afi_ptx_raw = None

b1afi_stx_raw = None