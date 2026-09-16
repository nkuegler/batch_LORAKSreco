#!/usr/bin/env python3

## subject names and session names
## if there are multiple sessions for a subject, the session names should be in a list
sub_ses = [["43472.ec", ["20250703_1", "20250703_2"]],
]

## directories of subjects and sessions for input and output
input_parent = "/data/p_03037/LORAKS_adults/source"
output_parent = "/data/p_03037/LORAKS_adults/source"
name_storage_dir = "nii_loraks_recon"   # name of the directory in the output_parent where the reconstructed data will be stored

with_smaps = True # boolean, specifies if sensitivity maps are also reconstructed
                   # each session file MUST have a corresponding sensitivity map file (2x length of t1w_raw, pdw_raw, mtw_raw)
                   # handled so that each specified session in sub_ses is used twice
smaps_per_session = 1 # integer, number of sensitivity maps per session

## specifying names of the actual pdw, t1w, mtw, and ernst .dat files
## Each one has to be a nested list, where the sessions of each subject are specified in a separate list.
pdw_raw = [[  # 43472.ec
              "meas_MID00102_FID142067_smaps_kp_mtflash3d_v1s_20ch.dat",        # 20250703_1
              "meas_MID00103_FID142068_pdw_kp_mtflash3d_v1s_1p0.dat",           # 20250703_1
              "placeholder.dat",        # 20250703_2
              "meas_MID00129_FID142094_pdw_kp_mtflash3d_v1s_1p0.dat",           # 20250703_2
           ]
]
           
t1w_raw = [[  # 43472.ec
              "meas_MID00100_FID142065_smaps_kp_mtflash3d_v1s_20ch.dat",        # 20250703_1
              "meas_MID00101_FID142066_t1w_kp_mtflash3d_v1s_1p0.dat",           # 20250703_1
              "meas_MID00126_FID142091_smaps_kp_mtflash3d_v1s_20ch.dat",        # 20250703_2
              "meas_MID00127_FID142092_t1w_kp_mtflash3d_v1s_1p0.dat",           # 20250703_2
           ]
]

mtw_raw = [[  # 43472.ec
              "meas_MID00104_FID142069_smaps_kp_mtflash3d_v1s_20ch.dat",           # 20250703_1
              "meas_MID00105_FID142070_mtw_kp_mtflash3d_v1s_1p0_FA180.dat",        # 20250703_1
              "placeholder.dat",           # 20250703_2
              "meas_MID00131_FID142096_mtw_kp_mtflash3d_v1s_1p0_FA180.dat",        # 20250703_2
           ]
]
ernst_raw = None

b1afi_ptx_raw = None

b1afi_stx_raw = None