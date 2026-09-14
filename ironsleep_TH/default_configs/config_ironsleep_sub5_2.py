#!/usr/bin/env python3

## subject names and session names
## if there are multiple sessions for a subject, the session names should be in a list
sub_ses = [["5perlaki", ["20241126_1", "20241126_2"]]
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
              "meas_MID00032_FID00039_pdw_kp_mtflash3d_v1s_0p6.dat",           # 20241126_1
              "meas_MID00070_FID00077_pdw_kp_mtflash3d_v1s_0p6.dat",           # 20241126_2
           ]
]
           
t1w_raw = [[  # 5perlaki
              "meas_MID00031_FID00038_t1w_kp_mtflash3d_v1s_0p6.dat",           # 20241126_1
              "meas_MID00069_FID00076_t1w_kp_mtflash3d_v1s_0p6.dat",           # 20241126_2
           ]
]

mtw_raw = [[  # 5perlaki
              "meas_MID00033_FID00040_mtw_kp_mtflash3d_v1s_0p6.dat",           # 20241126_1
              "meas_MID00071_FID00078_mtw_kp_mtflash3d_v1s_0p6.dat",           # 20241126_2
           ]
]

ernst_raw = [[  # 5perlaki
                "meas_MID00035_FID00042_ernst_kp_mtflash3d_v1s_0p5_sag.dat",           # 20241126_1
                "meas_MID00073_FID00080_ernst_kp_mtflash3d_v1s_0p5_sag.dat",           # 20241126_2
             ]
]

b1afi_ptx_raw = [[  # 5perlaki
                "meas_MID00034_FID00041_kp_afib1_v1g_4mm_PA.dat",           # 20241126_1
                "meas_MID00072_FID00079_kp_afib1_v1g_4mm_PA.dat",           # 20241126_2
             ]
]

b1afi_stx_raw = [[  # 5perlaki
                "meas_MID00039_FID00046_kp_afib1_v1g_4mm_PA_trueform.dat",           # 20241126_1
                "meas_MID00077_FID00084_kp_afib1_v1g_4mm_PA_trueform.dat",           # 20241126_2
             ]
]