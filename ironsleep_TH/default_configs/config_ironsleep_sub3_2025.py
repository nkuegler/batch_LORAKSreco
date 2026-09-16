#!/usr/bin/env python3

## subject names and session names
## if there are multiple sessions for a subject, the session names should be in a list
sub_ses = [["41486.2c", ["20250604", "20250611"]]
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
pdw_raw = [[  # 5perlaki
              "meas_MID00150_FID07571_pdw_kp_mtflash3d_v1s_0p6.dat",           # 20250604
              "meas_MID00085_FID08041_pdw_kp_mtflash3d_v1s_0p6.dat",           # 20250611
           ]
]
           
t1w_raw = [[  # 5perlaki
              "meas_MID00149_FID07570_t1w_kp_mtflash3d_v1s_0p6.dat",           # 20250604
              "meas_MID00084_FID08040_t1w_kp_mtflash3d_v1s_0p6.dat",           # 20250611
           ]
]

mtw_raw = [[  # 5perlaki
              "meas_MID00151_FID07572_mtw_kp_mtflash3d_v1s_0p6.dat",           # 20250604
              "meas_MID00086_FID08042_mtw_kp_mtflash3d_v1s_0p6.dat",           # 20250611
           ]
]

ernst_raw = [[  # 5perlaki
                "meas_MID00153_FID07574_ernst_kp_mtflash3d_v1s_0p5_sag.dat",           # 20250604
                "meas_MID00088_FID08044_ernst_kp_mtflash3d_v1s_0p5_sag.dat",           # 20250611
             ]
]

b1afi_ptx_raw = [[  # 5perlaki
                "meas_MID00152_FID07573_kp_afib1_v1g_4mm_PA.dat",           # 20250604
                "meas_MID00087_FID08043_kp_afib1_v1g_4mm_PA.dat",           # 20250611
             ]
]

b1afi_stx_raw = [[  # 5perlaki
                "meas_MID00160_FID07581_kp_afib1_v1g_4mm_PA_trueform.dat",           # 20250604 
                "meas_MID00092_FID08048_kp_afib1_v1g_4mm_PA_trueform.dat",           # 20250611
             ]
]