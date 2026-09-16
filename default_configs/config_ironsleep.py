#!/usr/bin/env python3

## subject names and session names
## if there are multiple sessions for a subject, the session names should be in a list
sub_ses = [["37446.6e", ["20230505","20230511","20230512","20240222"]],
           ["40851.ff", ["20230505","20230511","20230512","20240403"]],
           ["41006.a1", ["20230606","20231012","20231121","20231123"]],
           ["41486.2c", ["20230928","20231006","20231010"]],
]


## directories of subjects and sessions for input and output
input_parent = "/data/pt_02262/data/TH_bids/source/"
output_parent = "/data/pt_02262/data/TH_bids/source/"
name_storage_dir = "nii_loraks_recon"   # name of the directory in the output_parent where the reconstructed data will be stored

with_smaps = False # boolean, specifies if sensitivity maps are also reconstructed
                   # each session file MUST have a corresponding sensitivity map file (2x length of t1w_raw, pdw_raw, mtw_raw)
                   # handled so that each specified session in sub_ses is used twice
smaps_per_session = 0 # integer, number of sensitivity maps per session

## specifying names of the actual pdw, t1w, mtw, and ernst .dat files
## Each one has to be a nested list, where the sessions of each subject are specified in a separate list.
pdw_raw = [[  # 37446.6e  
              "meas_MID00159_pdw_kp_mtflash3d_v1sx_0p6_20230505_181529.dat",  # 20230505
              "meas_MID00089_FID17065_pdw_kp_mtflash3d_v1s_0p6.dat",          # 20230511
              "meas_MID00219_FID17220_pdw_kp_mtflash3d_v1s_0p6.dat",          # 20230512
              "meas_MeasUID45_pdw_kp_mtflash3d_v1sx_0p6.dat"                  # 20240222
           ],
           [  # 40851.ff
              "meas_MID00188_pdw_kp_mtflash3d_v1sx_0p6_20230505_193438.dat",  # 20230505
              "meas_MID00065_FID17041_pdw_kp_mtflash3d_v1s_0p6.dat",          # 20230511
              "meas_MID00169_FID17170_pdw_kp_mtflash3d_v1s_0p6.dat",          # 20230512
              "meas_MeasUID25_pdw_kp_mtflash3d_v1s_0p6.dat"                   # 20240403
           ],
           [  # 41006.a1 
              "meas_MeasUID111_pdw_kp_mtflash3d_v1sx_0p6.dat",               # 20230606
              "meas_MID00133_FID22399_pdw_kp_mtflash3d_v1s_0p6.dat",         # 20231012
              "meas_MID00116_pdw_kp_mtflash3d_v1sx_0p6_20231121-151338.dat", # 20231121
              "meas_MID00025_pdw_kp_mtflash3d_v1sx_0p6_20231123-203402.dat"  # 20231123
           ],
           [  # 41486.2c
              "meas_MID00025_pdw_kp_mtflash3d_v1sx_0p6_20230928-170046.dat", # 20230928
              "meas_MID00028_FID22300_pdw_kp_mtflash3d_v1s_0p6.dat",         # 20231006
              "meas_MID00075_FID22344_pdw_kp_mtflash3d_v1s_0p6.dat"          # 20231010
           ]
]
           
t1w_raw = [[  # 37446.6e
              "meas_MID00155_t1w_kp_mtflash3d_v1sx_0p6_20230505_180304.dat", # 20230505
              "meas_MID00088_FID17064_t1w_kp_mtflash3d_v1s_0p6.dat",         # 20230511
              "meas_MID00218_FID17219_t1w_kp_mtflash3d_v1s_0p6.dat",         # 20230512
              "meas_MeasUID44_t1w_kp_mtflash3d_v1sx_0p6.dat"                 # 20240222
           ],
           [  # 40851.ff
              "meas_MID00183_t1w_kp_mtflash3d_v1sx_0p6_20230505_192302.dat", # 20230505
              "meas_MID00064_FID17040_t1w_kp_mtflash3d_v1s_0p6.dat",         # 20230511
              "meas_MID00168_FID17169_t1w_kp_mtflash3d_v1s_0p6.dat",         # 20230512
              "meas_MeasUID24_t1w_kp_mtflash3d_v1s_0p6.dat",                 # 20240403
           ],
           [   # 41006.a1
               "meas_MeasUID108_t1w_kp_mtflash3d_v1sx_0p6.dat",             # 20230606
               "meas_MID00132_FID22398_t1w_kp_mtflash3d_v1s_0p6.dat",        # 20231012
               "meas_MID00115_t1w_kp_mtflash3d_v1sx_0p6_20231121-150148.dat",# 20231121
               "meas_MID00024_t1w_kp_mtflash3d_v1sx_0p6_20231123-202214.dat" # 20231123
           ],
           [   # 41486.2c
               "meas_MID00024_t1w_kp_mtflash3d_v1sx_0p6_20230928-164853.dat", # 20230928
               "meas_MID00027_FID22299_t1w_kp_mtflash3d_v1s_0p6.dat",         # 20231006
               "meas_MID00074_FID22343_t1w_kp_mtflash3d_v1s_0p6.dat"          # 20231010
           ]
]

mtw_raw = [[  # 37446.6e  
              "",  # 20230505
              "",  # 20230511
              "",  # 20230512
              "meas_MeasUID48_mtw_kp_mtflash3d_v1sx_0p6.dat"     # 20240222
           ],
           [  # 40851.ff
              "",  # 20230505
              "",          # 20230511
              "",          # 20230512
              "meas_MeasUID26_mtw_kp_mtflash3d_v1s_0p6.dat"      # 20240403
           ],
           [  # 41006.a1 
              "",               # 20230606
              "meas_MID00134_FID22400_mtw_kp_mtflash3d_v1s_0p6.dat",   # 20231012
              "meas_MID00118_mtw_kp_mtflash3d_v1sx_0p6_20231121-152631.dat", # 20231121
              "meas_MID00031_mtw_kp_mtflash3d_v1sx_0p6_20231123-204729.dat"  # 20231123
           ],
           [  # 41486.2c
              "", # 20230928
              "meas_MID00029_FID22301_mtw_kp_mtflash3d_v1s_0p6.dat",         # 20231006
              "meas_MID00077_FID22346_mtw_kp_mtflash3d_v1s_0p6.dat"          # 20231010
           ]
]

ernst_raw = [[  # 37446.6e
                "meas_MID00163_ernst_kp_mtflash3d_v1sx_0p5_sag_20230505_183143.dat", # 20230505
                "meas_MID00091_FID17067_ernst_kp_mtflash3d_v1s_0p5_sag.dat",     # 20230511
                "meas_MID00223_FID17224_ernst_kp_mtflash3d_v1s_0p5_sag.dat",     # 20230512
                "meas_MeasUID50_ernst_kp_mtflash3d_v1sx_0p5_sag.dat"             # 20240222
            ], 
            [  # 40851.ff
                "meas_MID00190_ernst_kp_mtflash3d_v1sx_0p5_sag_20230505_194708.dat", # 20230505
                "meas_MID00068_FID17044_ernst_kp_mtflash3d_v1s_0p5_sag.dat",     # 20230511
                "meas_MID00171_FID17172_ernst_kp_mtflash3d_v1s_0p5_sag.dat",     # 20230512
                "meas_MeasUID28_ernst_kp_mtflash3d_v1sx_0p5_sag.dat",            # 20240403
            ],
            [   # 41006.a1
                "meas_MeasUID116_ernst_kp_mtflash3d_v1sx_0p5_sag.dat",          # 20230606
                "meas_MID00136_FID22402_ernst_kp_mtflash3d_v1s_0p5_sag.dat",    # 20231012
                "meas_MID00134_ernst_kp_mtflash3d_v1sx_0p5_sag_20231121-154706.dat", # 20231121
                "meas_MID00033_ernst_kp_mtflash3d_v1sx_0p5_sag_20231123-210330.dat"  # 20231123
            ],
            [   # 41486.2c
                "meas_MID00027_ernst_kp_mtflash3d_v1sx_0p5_sag_20230928-171657.dat", # 20230928
                "meas_MID00031_FID22303_ernst_kp_mtflash3d_v1s_0p5_sag.dat",         # 20231006
                "meas_MID00079_FID22348_ernst_kp_mtflash3d_v1s_0p5_sag.dat"          # 20231010
            ]
]

b1afi_ptx_raw = [[  # 37446.6e  
              "meas_MID00161_kp_afib1_v1f_4mm_PA_20230505_182712.dat",  # 20230505
              "meas_MID00090_FID17066_kp_afib1_v1g_4mm_PA.dat",          # 20230511
              "meas_MID00222_FID17223_kp_afib1_v1g_4mm_PA.dat",          # 20230512
              "meas_MeasUID49_kp_afib1_v1f_4mm_PA.dat"                  # 20240222
           ],
           [  # 40851.ff
              "meas_MID00189_kp_afib1_v1f_4mm_PA_20230505_194315.dat",  # 20230505
              "meas_MID00066_FID17042_kp_afib1_v1g_4mm_PA.dat",         # 20230511
              "meas_MID00170_FID17171_kp_afib1_v1g_4mm_PA.dat",         # 20230512
              "meas_MeasUID27_kp_afib1_v1f_4mm_PA.dat"                  # 20240403
           ],
           [  # 41006.a1 
              "meas_MeasUID115_kp_afib1_v1f_4mm_PA.dat",               # 20230606
              "meas_MID00135_FID22401_kp_afib1_v1g_4mm_PA.dat",        # 20231012
              "meas_MID00119_kp_afib1_v1f_4mm_PA_20231121-153755.dat", # 20231121
              "meas_MID00032_kp_afib1_v1f_4mm_PA_20231123-205905.dat"  # 20231123
           ],
           [  # 41486.2c
              "meas_MID00026_kp_afib1_v1f_4mm_PA_20230928-171238.dat", # 20230928
              "",         # 20231006
              ""          # 20231010
           ]
]

b1afi_stx_raw = [[  # 37446.6e  
              "",  # 20230505
              "",  # 20230511
              "",  # 20230512
              "meas_MeasUID52_kp_afib1_v1f_4mm_PA_forT2.dat"         # 20240222
           ],
           [  # 40851.ff
              "",  # 20230505
              "",  # 20230511
              "meas_MID00178_FID17179_kp_afib1_v1g_4mm_PA_trueform.dat",   # 20230512
              "meas_MeasUID30_kp_afib1_v1f_4mm_PA_forT2.dat"               # 20240403
           ],
           [   # 41006.a1 
               "",               # 20230606
               "meas_MID00139_FID22405_kp_afib1_v1g_4mm_PA_trueform.dat",  # 20231012
               "meas_MID00140_kp_afib1_v1f_4mm_PA_forT2_20231121-161645.dat", # 20231121
               "meas_MID00037_kp_afib1_v1f_4mm_PA_forT2_20231123-213240.dat"  # 20231123
           ],
           [   # 41486.2c
               "meas_MID00029_kp_afib1_v1f_4mm_PA_forT2_20230928-174518.dat", # 20230928
               "",         # 20231006
               ""          # 20231010
           ]
]