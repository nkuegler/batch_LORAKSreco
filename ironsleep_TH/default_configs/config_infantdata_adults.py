#!/usr/bin/env python3

## subject names and session names
## if there are multiple sessions for a subject, the session names should be in a list
sub_ses = [["40851.ff", ["20250605_1", "20250605_2"]]
]

## directories of subjects and sessions for input and output
input_parent = "/data/p_03037/LORAKS_adults/source"
output_parent = "/data/p_03037/LORAKS_adults/source"
name_storage_dir = "nii_loraks_recon"   # name of the directory in the output_parent where the reconstructed data will be stored

with_smaps = True # boolean, specifies if sensitivity maps are also reconstructed
                   # each session file MUST have a corresponding sensitivity map file (2x length of t1w_raw, pdw_raw, mtw_raw)
                   # handled so that each specified session in sub_ses is used twice

## specifying names of the actual pdw, t1w, mtw, and ernst .dat files
## Each one has to be a nested list, where the sessions of each subject are specified in a separate list.
pdw_raw = [[  # 40851.ff
              "meas_MeasUID60_smaps_kp_mtflash3d_v1s_20ch_250605_100820.dat",        # 20250605_1
              "meas_MeasUID61_pdw_kp_mtflash3d_v1s_1p0_250605_100820.dat",           # 20250605_1
              "meas_MeasUID86_smaps_kp_mtflash3d_v1s_20ch_250605_100820.dat",        # 20250605_2
              "meas_MeasUID87_pdw_kp_mtflash3d_v1s_1p0_250605_100820.dat",           # 20250605_2
           ]
]
           
t1w_raw = [[  # 40851.ff
              "meas_MeasUID58_smaps_kp_mtflash3d_v1s_20ch_250605_100820.dat",        # 20250605_1
              "meas_MeasUID59_t1w_kp_mtflash3d_v1s_1p0_250605_100820.dat",           # 20250605_1
              "meas_MeasUID84_smaps_kp_mtflash3d_v1s_20ch_250605_100820.dat",        # 20250605_2
              "meas_MeasUID85_t1w_kp_mtflash3d_v1s_1p0_250605_100820.dat",           # 20250605_2
           ]
]

mtw_raw = [[  # 40851.ff
              "meas_MeasUID62_smaps_kp_mtflash3d_v1s_20ch_250605_100820.dat",           # 20250605_1
              "meas_MeasUID63_mtw_kp_mtflash3d_v1s_1p0_FA180_250605_100820.dat",        # 20250605_1
              "meas_MeasUID88_smaps_kp_mtflash3d_v1s_20ch_250605_100820.dat",           # 20250605_2
              "meas_MeasUID89_mtw_kp_mtflash3d_v1s_1p0_FA180_250605_100820.dat",        # 20250605_2
           ]
]
ernst_raw = None

b1afi_ptx_raw = None

b1afi_stx_raw = None