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
name_storage_dir = "nii_loraks_recon"   # name of the directory in the output_parent where the reconstructed data will be stored

with_smaps = True # boolean, specifies if sensitivity maps are also reconstructed
                   # each session file MUST have a corresponding sensitivity map file (2x length of t1w_raw, pdw_raw, mtw_raw)
                   # handled so that each specified session in sub_ses is used twice
smaps_per_session = 1 # integer, number of sensitivity maps per session

## specifying names of the actual pdw, t1w, mtw, and ernst .dat files
## Each one has to be a nested list, where the sessions of each subject are specified in a separate list.
pdw_raw = [[   # 22194.ff
               "meas_MeasUID28_smaps_kp_mtflash3d_v1s_20ch_250902_073957.dat",        # 20250902_1
               "meas_MeasUID29_pdw_kp_mtflash3d_v1s_1p0_250902_073957.dat",           # 20250902_1
               "meas_MeasUID54_smaps_kp_mtflash3d_v1s_20ch_250902_073957.dat",        # 20250902_2
               "meas_MeasUID55_pdw_kp_mtflash3d_v1s_1p0_250902_073957.dat",           # 20250902_2
           ],
           [   # 42577.9a
               "meas_MeasUID105_smaps_kp_mtflash3d_v1s_20ch_250902_102716.dat",      # 20250902_2
               "meas_MeasUID106_pdw_kp_mtflash3d_v1s_1p0_250902_102716.dat",         # 20250902_2
           ],
           [   # 36881.c9
               "meas_MeasUID130_smaps_kp_mtflash3d_v1s_20ch_250902_115027.dat",      # 20250902_1
               "meas_MeasUID131_pdw_kp_mtflash3d_v1s_1p0_250902_115027.dat",         # 20250902_1
               "meas_MeasUID156_smaps_kp_mtflash3d_v1s_20ch_250902_115027.dat",      # 20250902_2
               "meas_MeasUID157_pdw_kp_mtflash3d_v1s_1p0_250902_115027.dat",         # 20250902_2
           ],
           [   # 39626.d6
               "meas_MeasUID27_smaps_kp_mtflash3d_v1s_20ch_250903_074031.dat",      # 20250903_1
               "meas_MeasUID28_pdw_kp_mtflash3d_v1s_1p0_250903_074031.dat",         # 20250903_1
               "meas_MeasUID53_smaps_kp_mtflash3d_v1s_20ch_250903_074031.dat",      # 20250903_2
               "meas_MeasUID54_pdw_kp_mtflash3d_v1s_1p0_250903_074031.dat",         # 20250903_2
           ],
           [   # 43306.68
               "meas_MeasUID104_smaps_kp_mtflash3d_v1s_20ch_250903_091814.dat",      # 20250903_1
               "meas_MeasUID105_pdw_kp_mtflash3d_v1s_1p0_250903_091814.dat",         # 20250903_1
               "meas_MeasUID123_smaps_kp_mtflash3d_v1s_20ch_250903_091814.dat",      # 20250903_2
               "meas_MeasUID124_pdw_kp_mtflash3d_v1s_1p0_250903_091814.dat",         # 20250903_2
               "meas_MeasUID78_smaps_kp_mtflash3d_v1s_20ch_250903_091814.dat",     # 20250903_3
               "meas_MeasUID79_pdw_kp_mtflash3d_v1s_1p0_250903_091814.dat",        # 20250903_3
           ],
           [   # 43081.e5
               "meas_MeasUID148_smaps_kp_mtflash3d_v1s_20ch_250903_133935.dat",      # 20250903_1
               "meas_MeasUID149_pdw_kp_mtflash3d_v1s_1p0_250903_133935.dat",         # 20250903_1
               "meas_MeasUID174_smaps_kp_mtflash3d_v1s_20ch_250903_133935.dat",      # 20250903_2
               "meas_MeasUID175_pdw_kp_mtflash3d_v1s_1p0_250903_133935.dat",         # 20250903_2
           ],
           [   # 43474.c0
               "meas_MeasUID27_smaps_kp_mtflash3d_v1s_20ch_250904_105011.dat",      # 20250904_1
               "meas_MeasUID28_pdw_kp_mtflash3d_v1s_1p0_250904_105011.dat",         # 20250904_1
               "meas_MeasUID53_smaps_kp_mtflash3d_v1s_20ch_250904_105011.dat",      # 20250904_2
               "meas_MeasUID54_pdw_kp_mtflash3d_v1s_1p0_250904_105011.dat",         # 20250904_2
           ],
           [   # 34522.15
               "meas_MeasUID113_smaps_kp_mtflash3d_v1s_20ch_250904_131043.dat",      # 20250904_1
               "meas_MeasUID114_pdw_kp_mtflash3d_v1s_1p0_250904_131043.dat",         # 20250904_1
               "meas_MeasUID140_smaps_kp_mtflash3d_v1s_20ch_250904_131043.dat",      # 20250904_2
               "meas_MeasUID141_pdw_kp_mtflash3d_v1s_1p0_250904_131043.dat",         # 20250904_2
           ],
           [   # 38787.07
               "meas_MeasUID165_smaps_kp_mtflash3d_v1s_20ch_250904_150941.dat",     # 20250904_1
               "meas_MeasUID166_pdw_kp_mtflash3d_v1s_1p0_250904_150941.dat",     # 20250904_1
               "meas_MeasUID191_smaps_kp_mtflash3d_v1s_20ch_250904_150941.dat",     # 20250904_2
               "meas_MeasUID192_pdw_kp_mtflash3d_v1s_1p0_250904_150941.dat",     # 20250904_2
           ],
           [   # 37463.22
               "meas_MeasUID28_smaps_kp_mtflash3d_v1s_20ch_250905_080758.dat",   # 20250905_1
               "meas_MeasUID29_pdw_kp_mtflash3d_v1s_1p0_250905_080758.dat",   # 20250905_1
               "meas_MeasUID54_smaps_kp_mtflash3d_v1s_20ch_250905_080758.dat",   # 20250905_2
               "meas_MeasUID55_pdw_kp_mtflash3d_v1s_1p0_250905_080758.dat",   # 20250905_2
           ],
           [   # 19925.e6
               "meas_MeasUID27_smaps_kp_mtflash3d_v1s_20ch_250918_113005.dat",   # 20250918_1
               "meas_MeasUID28_pdw_kp_mtflash3d_v1s_1p0_250918_113005.dat",       # 20250918_1
               "meas_MeasUID53_smaps_kp_mtflash3d_v1s_20ch_250918_113005.dat",   # 20250918_2
               "meas_MeasUID54_pdw_kp_mtflash3d_v1s_1p0_250918_113005.dat",       # 20250918_2
           ],
]

t1w_raw = [[   # 22194.ff
               "meas_MeasUID26_smaps_kp_mtflash3d_v1s_20ch_250902_073957.dat",        # 20250902_1
               "meas_MeasUID27_t1w_kp_mtflash3d_v1s_1p0_250902_073957.dat",           # 20250902_1
               "meas_MeasUID52_smaps_kp_mtflash3d_v1s_20ch_250902_073957.dat",        # 20250902_2
               "meas_MeasUID53_t1w_kp_mtflash3d_v1s_1p0_250902_073957.dat",           # 20250902_2
           ],
           [   # 42577.9a
               "meas_MeasUID103_smaps_kp_mtflash3d_v1s_20ch_250902_102716.dat",        # 20250902_2
               "meas_MeasUID104_t1w_kp_mtflash3d_v1s_1p0_250902_102716.dat",           # 20250902_2
           ],
           [   # 36881.c9
               "meas_MeasUID128_smaps_kp_mtflash3d_v1s_20ch_250902_115027.dat",        # 20250902_1
               "meas_MeasUID129_t1w_kp_mtflash3d_v1s_1p0_250902_115027.dat",           # 20250902_1
               "meas_MeasUID154_smaps_kp_mtflash3d_v1s_20ch_250902_115027.dat",        # 20250902_2
               "meas_MeasUID155_t1w_kp_mtflash3d_v1s_1p0_250902_115027.dat",           # 20250902_2
           ],
           [   # 39626.d6
               "meas_MeasUID25_smaps_kp_mtflash3d_v1s_20ch_250903_074031.dat",      # 20250903_1
               "meas_MeasUID26_t1w_kp_mtflash3d_v1s_1p0_250903_074031.dat",         # 20250903_1
               "meas_MeasUID51_smaps_kp_mtflash3d_v1s_20ch_250903_074031.dat",      # 20250903_2
               "meas_MeasUID52_t1w_kp_mtflash3d_v1s_1p0_250903_074031.dat",         # 20250903_2
           ],
           [   # 43306.68
               "meas_MeasUID102_smaps_kp_mtflash3d_v1s_20ch_250903_091814.dat",      # 20250903_1
               "meas_MeasUID103_t1w_kp_mtflash3d_v1s_1p0_250903_091814.dat",         # 20250903_1
               "meas_MeasUID116_smaps_kp_mtflash3d_v1s_20ch_250903_091814.dat",      # 20250903_2
               "meas_MeasUID117_t1w_kp_mtflash3d_v1s_1p0_250903_091814.dat",         # 20250903_2
               "",     # 20250903_3
               "",        # 20250903_3
           ],
           [   # 43081.e5
               "meas_MeasUID146_smaps_kp_mtflash3d_v1s_20ch_250903_133935.dat",      # 20250903_1
               "meas_MeasUID147_t1w_kp_mtflash3d_v1s_1p0_250903_133935.dat",         # 20250903_1
               "meas_MeasUID172_smaps_kp_mtflash3d_v1s_20ch_250903_133935.dat",      # 20250903_2
               "meas_MeasUID173_t1w_kp_mtflash3d_v1s_1p0_250903_133935.dat",         # 20250903_2
           ],
           [   # 43474.c0
               "meas_MeasUID25_smaps_kp_mtflash3d_v1s_20ch_250904_105011.dat",      # 20250904_1
               "meas_MeasUID26_t1w_kp_mtflash3d_v1s_1p0_250904_105011.dat",         # 20250904_1
               "meas_MeasUID51_smaps_kp_mtflash3d_v1s_20ch_250904_105011.dat",      # 20250904_2
               "meas_MeasUID52_t1w_kp_mtflash3d_v1s_1p0_250904_105011.dat",         # 20250904_2
           ],
           [   # 34522.15
               "meas_MeasUID111_smaps_kp_mtflash3d_v1s_20ch_250904_131043.dat",      # 20250904_1
               "meas_MeasUID112_t1w_kp_mtflash3d_v1s_1p0_250904_131043.dat",         # 20250904_1
               "meas_MeasUID138_smaps_kp_mtflash3d_v1s_20ch_250904_131043.dat",      # 20250904_2
               "meas_MeasUID139_t1w_kp_mtflash3d_v1s_1p0_250904_131043.dat",         # 20250904_2
           ],
           [   # 38787.07
               "meas_MeasUID163_smaps_kp_mtflash3d_v1s_20ch_250904_150941.dat",     # 20250904_1
               "meas_MeasUID164_t1w_kp_mtflash3d_v1s_1p0_250904_150941.dat",     # 20250904_1
               "meas_MeasUID189_smaps_kp_mtflash3d_v1s_20ch_250904_150941.dat",     # 20250904_2
               "meas_MeasUID190_t1w_kp_mtflash3d_v1s_1p0_250904_150941.dat",     # 20250904_2
           ],
           [   # 37463.22
               "meas_MeasUID26_smaps_kp_mtflash3d_v1s_20ch_250905_080758.dat",   # 20250905_1
               "meas_MeasUID27_t1w_kp_mtflash3d_v1s_1p0_250905_080758.dat",   # 20250905_1
               "meas_MeasUID52_smaps_kp_mtflash3d_v1s_20ch_250905_080758.dat",   # 20250905_2
               "meas_MeasUID53_t1w_kp_mtflash3d_v1s_1p0_250905_080758.dat",   # 20250905_2
           ],
           [   # 19925.e6
               "meas_MeasUID25_smaps_kp_mtflash3d_v1s_20ch_250918_113005.dat",   # 20250918_1
               "meas_MeasUID26_t1w_kp_mtflash3d_v1s_1p0_250918_113005.dat",       # 20250918_1
               "meas_MeasUID51_smaps_kp_mtflash3d_v1s_20ch_250918_113005.dat",   # 20250918_2
               "meas_MeasUID52_t1w_kp_mtflash3d_v1s_1p0_250918_113005.dat",       # 20250918_2
           ],
] 

mtw_raw = [[   # 22194.ff
               "meas_MeasUID30_smaps_kp_mtflash3d_v1s_20ch_250902_073957.dat",           # 20250902_1
               "meas_MeasUID31_mtw_kp_mtflash3d_v1s_1p0_FA180_250902_073957.dat",        # 20250902_1
               "meas_MeasUID56_smaps_kp_mtflash3d_v1s_20ch_250902_073957.dat",           # 20250902_2
               "meas_MeasUID57_mtw_kp_mtflash3d_v1s_1p0_FA180_250902_073957.dat",        # 20250902_2
           ],
           [   # 42577.9a
               "meas_MeasUID107_smaps_kp_mtflash3d_v1s_20ch_250902_102716.dat",        # 20250902_2
               "meas_MeasUID108_mtw_kp_mtflash3d_v1s_1p0_FA180_250902_102716.dat",     # 20250902_2
           ],
           [   # 36881.c9
               "meas_MeasUID132_smaps_kp_mtflash3d_v1s_20ch_250902_115027.dat",        # 20250902_1
               "meas_MeasUID133_mtw_kp_mtflash3d_v1s_1p0_FA180_250902_115027.dat",     # 20250902_1
               "meas_MeasUID158_smaps_kp_mtflash3d_v1s_20ch_250902_115027.dat",        # 20250902_2
               "meas_MeasUID159_mtw_kp_mtflash3d_v1s_1p0_FA180_250902_115027.dat",      # 20250902_2
           ],
           [   # 39626.d6
               "meas_MeasUID29_smaps_kp_mtflash3d_v1s_20ch_250903_074031.dat",      # 20250903_1
               "meas_MeasUID30_mtw_kp_mtflash3d_v1s_1p0_FA180_250903_074031.dat",     # 20250903_1
               "meas_MeasUID55_smaps_kp_mtflash3d_v1s_20ch_250903_074031.dat",      # 20250903_2
               "meas_MeasUID56_mtw_kp_mtflash3d_v1s_1p0_FA180_250903_074031.dat",     # 20250903_2
           ],
           [   # 43306.68
               "meas_MeasUID106_smaps_kp_mtflash3d_v1s_20ch_250903_091814.dat",      # 20250903_1
               "meas_MeasUID107_mtw_kp_mtflash3d_v1s_1p0_FA180_250903_091814.dat",         # 20250903_1
               "meas_MeasUID125_smaps_kp_mtflash3d_v1s_20ch_250903_091814.dat",      # 20250903_2
               "meas_MeasUID126_mtw_kp_mtflash3d_v1s_1p0_FA180_250903_091814.dat",         # 20250903_2
               "meas_MeasUID80_smaps_kp_mtflash3d_v1s_20ch_250903_091814.dat",     # 20250903_3
               "meas_MeasUID81_mtw_kp_mtflash3d_v1s_1p0_FA180_250903_091814.dat",        # 20250903_3
           ],
           [   # 43081.e5
               "meas_MeasUID150_smaps_kp_mtflash3d_v1s_20ch_250903_133935.dat",      # 20250903_1
               "meas_MeasUID151_mtw_kp_mtflash3d_v1s_1p0_FA180_250903_133935.dat",         # 20250903_1
               "meas_MeasUID176_smaps_kp_mtflash3d_v1s_20ch_250903_133935.dat",      # 20250903_2
               "meas_MeasUID177_mtw_kp_mtflash3d_v1s_1p0_FA180_250903_133935.dat",         # 20250903_2
           ],
           [   # 43474.c0
               "meas_MeasUID29_smaps_kp_mtflash3d_v1s_20ch_250904_105011.dat",      # 20250904_1
               "meas_MeasUID30_mtw_kp_mtflash3d_v1s_1p0_FA180_250904_105011.dat",         # 20250904_1
               "meas_MeasUID55_smaps_kp_mtflash3d_v1s_20ch_250904_105011.dat",      # 20250904_2
               "meas_MeasUID56_mtw_kp_mtflash3d_v1s_1p0_FA180_250904_105011.dat",         # 20250904_2
           ],
           [   # 34522.15
               "meas_MeasUID115_smaps_kp_mtflash3d_v1s_20ch_250904_131043.dat",      # 20250904_1
               "meas_MeasUID117_mtw_kp_mtflash3d_v1s_1p0_FA180_250904_131043.dat",         # 20250904_1
               "meas_MeasUID142_smaps_kp_mtflash3d_v1s_20ch_250904_131043.dat",      # 20250904_2
               "meas_MeasUID143_mtw_kp_mtflash3d_v1s_1p0_FA180_250904_131043.dat",         # 20250904_2
           ],
           [   # 38787.07
               "meas_MeasUID167_smaps_kp_mtflash3d_v1s_20ch_250904_150941.dat",     # 20250904_1
               "meas_MeasUID168_mtw_kp_mtflash3d_v1s_1p0_FA180_250904_150941.dat",     # 20250904_1
               "meas_MeasUID193_smaps_kp_mtflash3d_v1s_20ch_250904_150941.dat",     # 20250904_2
               "meas_MeasUID194_mtw_kp_mtflash3d_v1s_1p0_FA180_250904_150941.dat",     # 20250904_2
           ],
           [   # 37463.22
               "meas_MeasUID30_smaps_kp_mtflash3d_v1s_20ch_250905_080758.dat",   # 20250905_1
               "meas_MeasUID31_mtw_kp_mtflash3d_v1s_1p0_FA180_250905_080758.dat",   # 20250905_1
               "meas_MeasUID56_smaps_kp_mtflash3d_v1s_20ch_250905_080758.dat",   # 20250905_2
               "meas_MeasUID57_mtw_kp_mtflash3d_v1s_1p0_FA180_250905_080758.dat",   # 20250905_2
           ],
           [   # 19925.e6
               "meas_MeasUID29_smaps_kp_mtflash3d_v1s_20ch_250918_113005.dat",   # 20250918_1
               "meas_MeasUID30_mtw_kp_mtflash3d_v1s_1p0_FA180_250918_113005.dat",       # 20250918_1
               "meas_MeasUID55_smaps_kp_mtflash3d_v1s_20ch_250918_113005.dat",   # 20250918_2
               "meas_MeasUID56_mtw_kp_mtflash3d_v1s_1p0_FA180_250918_113005.dat",       # 20250918_2
           ],
          ]

ernst_raw = None

b1afi_ptx_raw = None

b1afi_stx_raw = None