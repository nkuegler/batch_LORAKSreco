#!/usr/bin/env python3

## subject names and session names
## if there are multiple sessions for a subject, the session names should be in a list
sub_ses = [["43155.b4", ["20250221"]],
           ["43182.89", ["20250305"]],
           ["43396.48", ["20250526"]],
           ["43397.f2", ["20250526"]],
]

## directories of subjects and sessions for input and output
input_parent = "/data/pt_03068/data/in_vivo/source"
output_parent = "/data/pt_03068/data/in_vivo/source"
name_storage_dir = "nii_loraks_recon"   # name of the directory in the output_parent where the reconstructed data will be stored

with_smaps = True # boolean, specifies if sensitivity maps are also reconstructed
                   # each session file MUST have a corresponding sensitivity map file (2x length of t1w_raw, pdw_raw, mtw_raw)
                   # handled so that each specified session in sub_ses is used twice
smaps_per_session = 1 # integer, number of sensitivity maps per session

## specifying names of the actual pdw, t1w, mtw, and ernst .dat files
## Each one has to be a nested list, where the sessions of each subject are specified in a separate list.
pdw_raw = [[   # 43155.b4
               "meas_MeasUID88_smap_kp_mtflash3d_v1s_4p0_250221_124014.dat",    # 20250221
               "meas_MeasUID89_pdw_kp_mtflash3d_v1s_0p6_250221_124014.dat",     # 20250221
           ],
           [   # 43182.89
               "meas_MeasUID47_smap_kp_mtflash3d_v1s_4p0_250305_082729.dat",    # 20250305
               "meas_MeasUID48_pdw_kp_mtflash3d_v1s_0p6_250305_082729.dat",     # 20250305 
           ],
           [   # 43396.48
               "meas_MeasUID263_smap_kp_mtflash3d_v1s_4p0_250526_175041.dat",   # 20250526
               "meas_MeasUID264_pdw_kp_mtflash3d_v1s_0p6_250526_175041.dat",    # 20250526
           ],
           [   # 43397.f2
               "meas_MeasUID235_smap_kp_mtflash3d_v1s_4p0_250526_165233.dat",         # 20250526
               "meas_MeasUID236_pdw_kp_mtflash3d_v1s_0p6_250526_165233.dat",         # 20250526
           ],
]

t1w_raw = [[   # 43155.b4
               "meas_MeasUID86_smap_kp_mtflash3d_v1s_4p0_250221_124014.dat",    # 20250221
               "meas_MeasUID87_t1w_kp_mtflash3d_v1s_0p6_250221_124014.dat",     # 20250221
           ],
           [   # 43182.89
               "meas_MeasUID45_smap_kp_mtflash3d_v1s_4p0_250305_082729.dat",    # 20250305
               "meas_MeasUID46_t1w_kp_mtflash3d_v1s_0p6_250305_082729.dat",     # 20250305
           ],
           [   # 43396.48
               "meas_MeasUID261_smap_kp_mtflash3d_v1s_4p0_250526_175041.dat",   # 20250526
               "meas_MeasUID262_t1w_kp_mtflash3d_v1s_0p6_250526_175041.dat",    # 20250526
           ],
           [   # 43397.f2
               "meas_MeasUID233_smap_kp_mtflash3d_v1s_4p0_250526_165233.dat",         # 20250526
               "meas_MeasUID234_t1w_kp_mtflash3d_v1s_0p6_250526_165233.dat",         # 20250526
           ],
] 

mtw_raw = [[   # 43155.b4
               "meas_MeasUID90_smap_kp_mtflash3d_v1s_4p0_250221_124014.dat",    # 20250221
               "meas_MeasUID91_mtw_kp_mtflash3d_v1s_0p6_250221_124014.dat",     # 20250221
           ],
           [   # 43182.89
               "meas_MeasUID49_smap_kp_mtflash3d_v1s_4p0_250305_082729.dat",    # 20250305
               "meas_MeasUID54_mtw_kp_mtflash3d_v1s_0p6_250305_082729.dat",     # 20250305
           ],
           [   # 43396.48
               "meas_MeasUID265_smap_kp_mtflash3d_v1s_4p0_250526_175041.dat",   # 20250526
               "meas_MeasUID266_mtw_kp_mtflash3d_v1s_0p6_250526_175041.dat",    # 20250526
           ],
           [   # 43397.f2
               "meas_MeasUID237_smap_kp_mtflash3d_v1s_4p0_250526_165233.dat",     # 20250526
               "meas_MeasUID239_mtw_kp_mtflash3d_v1s_0p6_250526_165233.dat",     # 20250526
           ],
]

ernst_raw = None

b1afi_ptx_raw = None

b1afi_stx_raw = None