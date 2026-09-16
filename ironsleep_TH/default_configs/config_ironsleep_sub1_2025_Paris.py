#!/usr/bin/env python3

## subject names and session names
## if there are multiple sessions for a subject, the session names should be in a list
sub_ses = [["40851.ff", ["20251027_1", "20251027_2"]]
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
pdw_raw = [[  # 40851.ff
              "meas_MID00105_FID05302_pdw_kp_mtflash3d_v1s_0p6.dat",           # 20251027_1
              "meas_MID00145_FID05342_pdw_kp_mtflash3d_v1s_0p6.dat",           # 20251027_2
           ]
]
           
t1w_raw = [[  # 40851.ff
              "meas_MID00104_FID05301_t1w_kp_mtflash3d_v1s_0p6.dat",           # 20251027_1
              "meas_MID00144_FID05341_t1w_kp_mtflash3d_v1s_0p6.dat",           # 20251027_2
           ]
]

mtw_raw = [[  # 40851.ff
              "meas_MID00106_FID05303_mtw_kp_mtflash3d_v1s_0p6.dat",           # 20251027_1
              "meas_MID00147_FID05344_mtw_kp_mtflash3d_v1s_0p6.dat",           # 20251027_2
           ]
]

ernst_raw = [[  # 40851.ff
                "meas_MID00108_FID05305_ernst_kp_mtflash3d_v1s_0p5_sag.dat",           # 20251027_1
                "meas_MID00149_FID05346_ernst_kp_mtflash3d_v1s_0p5_sag.dat",           # 20251027_2
             ]
]

b1afi_ptx_raw = None

b1afi_stx_raw = None