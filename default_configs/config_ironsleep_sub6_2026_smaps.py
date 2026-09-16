#!/usr/bin/env python3

## subject names and session names
## if there are multiple sessions for a subject, the session names should be in a list
sub_ses = [["43502.a2", ["20251211"]],
]

## directories of subjects and sessions for input and output
input_parent = "/data/pt_02262/data/TH_bids/source"
output_parent = "/data/pt_02262/data/TH_bids/source"
name_storage_dir = "nii_loraks_recon_smaps"   # name of the directory in the output_parent where the reconstructed data will be stored

with_smaps = True # boolean, specifies if sensitivity maps are also reconstructed
                   # each session file MUST have a corresponding sensitivity map file (2x length of t1w_raw, pdw_raw, mtw_raw)
                   # handled so that each specified session in sub_ses is used twice
smaps_per_session = 1 # integer, number of sensitivity maps per session

## specifying names of the actual pdw, t1w, mtw, and ernst .dat files
## Each one has to be a nested list, where the sessions of each subject are specified in a separate list.
pdw_raw = [[  # 43502.a2
              "meas_MeasUID57_smaps_kp_mtflash3d_v1s_BC_251211_121909.dat",    # 20251211
              "meas_MeasUID58_smaps_kp_mtflash3d_v1s_32Ch_251211_121909.dat",   # 20251211
           ], 
        ]

t1w_raw = [[  # 43502.a2
              "meas_MeasUID54_smaps_kp_mtflash3d_v1s_BC_251211_121909.dat",    # 20251211
              "meas_MeasUID55_smaps_kp_mtflash3d_v1s_32Ch_251211_121909.dat",   # 20251211
           ], 
        ]

mtw_raw = [[   # 43502.a2
               "meas_MeasUID60_smaps_kp_mtflash3d_v1s_BC_251211_121909.dat",    # 20251211
               "meas_MeasUID61_smaps_kp_mtflash3d_v1s_32Ch_251211_121909.dat",   # 20251211
           ], 
        ]

ernst_raw = None

b1afi_ptx_raw = None

b1afi_stx_raw = None