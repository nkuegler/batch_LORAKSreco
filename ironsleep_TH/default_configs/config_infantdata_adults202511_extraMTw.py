#!/usr/bin/env python3

## subject names and session names
## if there are multiple sessions for a subject, the session names should be in a list
sub_ses = [["22194.ff", ["20250902_1", "20250902_2"]],
           ["42577.9a", ["20250902_2"]],
           ["36881.c9", ["20250902_1", "20250902_2"]],
           ["39626.d6", ["20250903_1", "20250903_2"]],
           ["43306.68", ["20250903_1", "20250903_2", "20250903_3"]],
           ["43081.e5", ["20250903_1", "20250903_2"]],
           ["43474.c0", ["20250904_1", "20250904_2"]],
           ["34522.15", ["20250904_1", "20250904_2"]],
           ["38787.07", ["20250904_1", "20250904_2"]],
           ["37463.22", ["20250905_1", "20250905_2"]],
           ["19925.e6", ["20250918_1", "20250918_2"]],
]

## directories of subjects and sessions for input and output
input_parent = "/data/p_03037/LORAKS_adults/source"
output_parent = "/data/p_03037/LORAKS_adults/source"
name_storage_dir = "nii_loraks_recon_extraMTw"   # name of the directory in the output_parent where the reconstructed data will be stored

with_smaps = True # boolean, specifies if sensitivity maps are also reconstructed
                   # each session file MUST have a corresponding sensitivity map file (2x length of t1w_raw, pdw_raw, mtw_raw)
                   # handled so that each specified session in sub_ses is used twice
smaps_per_session = 1 # integer, number of sensitivity maps per session

## specifying names of the actual pdw, t1w, mtw, and ernst .dat files
## Each one has to be a nested list, where the sessions of each subject are specified in a separate list.
pdw_raw = None
           
t1w_raw = None

mtw_raw = [[   # 22194.ff
               "meas_MeasUID32_smaps_kp_mtflash3d_v1s_20ch_250902_073957.dat",        # 20250902_1
               "meas_MeasUID33_mtw_kp_mtflash3d_v1s_1p0_fa220_250902_073957.dat",     # 20250902_1
               "meas_MeasUID58_smaps_kp_mtflash3d_v1s_20ch_250902_073957.dat",        # 20250902_2
               "meas_MeasUID59_mtw_kp_mtflash3d_v1s_1p0_fa220_250902_073957.dat",     # 20250902_2
           ],
           [   # 42577.9a
               "meas_MeasUID109_smaps_kp_mtflash3d_v1s_20ch_250902_102716.dat",        # 20250902_2
               "meas_MeasUID110_mtw_kp_mtflash3d_v1s_1p0_fa220_250902_102716.dat",     # 20250902_2
           ],
           [   # 36881.c9
               "meas_MeasUID134_smaps_kp_mtflash3d_v1s_20ch_250902_115027.dat",        # 20250902_1
               "meas_MeasUID135_mtw_kp_mtflash3d_v1s_1p0_fa220_250902_115027.dat",     # 20250902_1
               "meas_MeasUID160_smaps_kp_mtflash3d_v1s_20ch_250902_115027.dat",        # 20250902_2
               "meas_MeasUID161_mtw_kp_mtflash3d_v1s_1p0_fa220_250902_115027.dat",      # 20250902_2
           ],
           [   # 39626.d6
               "meas_MeasUID31_smaps_kp_mtflash3d_v1s_20ch_250903_074031.dat",      # 20250903_1
               "meas_MeasUID32_mtw_kp_mtflash3d_v1s_1p0_fa220_250903_074031.dat",     # 20250903_1
               "meas_MeasUID57_smaps_kp_mtflash3d_v1s_20ch_250903_074031.dat",      # 20250903_2
               "meas_MeasUID58_mtw_kp_mtflash3d_v1s_1p0_fa220_250903_074031.dat",     # 20250903_2
           ],
           [   # 43306.68
               "meas_MeasUID108_smaps_kp_mtflash3d_v1s_20ch_250903_091814.dat",      # 20250903_1
               "meas_MeasUID109_mtw_kp_mtflash3d_v1s_1p0_fa220_250903_091814.dat",         # 20250903_1
               "meas_MeasUID127_smaps_kp_mtflash3d_v1s_20ch_250903_091814.dat",      # 20250903_2
               "meas_MeasUID128_mtw_kp_mtflash3d_v1s_1p0_fa220_250903_091814.dat",         # 20250903_2
               "meas_MeasUID82_smaps_kp_mtflash3d_v1s_20ch_250903_091814.dat",    # 20250903_3
               "meas_MeasUID83_mtw_kp_mtflash3d_v1s_1p0_fa220_250903_091814.dat",       # 20250903_3
           ],
           [   # 43081.e5
               "meas_MeasUID152_smaps_kp_mtflash3d_v1s_20ch_250903_133935.dat",      # 20250903_1
               "meas_MeasUID153_mtw_kp_mtflash3d_v1s_1p0_fa220_250903_133935.dat",         # 20250903_1
               "meas_MeasUID178_smaps_kp_mtflash3d_v1s_20ch_250903_133935.dat",      # 20250903_2
               "meas_MeasUID179_mtw_kp_mtflash3d_v1s_1p0_fa220_250903_133935.dat",         # 20250903_2
           ],
           [   # 43474.c0
               "meas_MeasUID31_smaps_kp_mtflash3d_v1s_20ch_250904_105011.dat",      # 20250904_1
               "meas_MeasUID32_mtw_kp_mtflash3d_v1s_1p0_fa220_250904_105011.dat",         # 20250904_1
               "meas_MeasUID57_smaps_kp_mtflash3d_v1s_20ch_250904_105011.dat",      # 20250904_2
               "meas_MeasUID58_mtw_kp_mtflash3d_v1s_1p0_fa220_250904_105011.dat",         # 20250904_2
           ],
           [   # 34522.15
               "meas_MeasUID118_smaps_kp_mtflash3d_v1s_20ch_250904_131043.dat",      # 20250904_1
               "meas_MeasUID119_mtw_kp_mtflash3d_v1s_1p0_fa220_250904_131043.dat",         # 20250904_1
               "meas_MeasUID144_smaps_kp_mtflash3d_v1s_20ch_250904_131043.dat",      # 20250904_2
               "meas_MeasUID145_mtw_kp_mtflash3d_v1s_1p0_fa220_250904_131043.dat",         # 20250904_2
           ],
           [   # 38787.07
               "meas_MeasUID169_smaps_kp_mtflash3d_v1s_20ch_250904_150941.dat",     # 20250904_1
               "meas_MeasUID170_mtw_kp_mtflash3d_v1s_1p0_fa220_250904_150941.dat",     # 20250904_1
               "meas_MeasUID195_smaps_kp_mtflash3d_v1s_20ch_250904_150941.dat",     # 20250904_2
               "meas_MeasUID196_mtw_kp_mtflash3d_v1s_1p0_fa220_250904_150941.dat",     # 20250904_2
           ],
           [   # 37463.22
               "meas_MeasUID32_smaps_kp_mtflash3d_v1s_20ch_250905_080758.dat",   # 20250905_1
               "meas_MeasUID33_mtw_kp_mtflash3d_v1s_1p0_fa220_250905_080758.dat",   # 20250905_1
               "meas_MeasUID58_smaps_kp_mtflash3d_v1s_20ch_250905_080758.dat",   # 20250905_2
               "meas_MeasUID59_mtw_kp_mtflash3d_v1s_1p0_fa220_250905_080758.dat",   # 20250905_2
           ],
           [   # 19925.e6
               "meas_MeasUID31_smaps_kp_mtflash3d_v1s_20ch_250918_113005.dat",   # 20250918_1
               "meas_MeasUID32_mtw_kp_mtflash3d_v1s_1p0_fa220_250918_113005.dat",       # 20250918_1
               "meas_MeasUID57_smaps_kp_mtflash3d_v1s_20ch_250918_113005.dat",   # 20250918_2
               "meas_MeasUID58_mtw_kp_mtflash3d_v1s_1p0_fa220_250918_113005.dat",       # 20250918_2
           ],
]
ernst_raw = None

b1afi_ptx_raw = None

b1afi_stx_raw = None