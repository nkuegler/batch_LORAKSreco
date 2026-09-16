#!/usr/bin/env python3

## subject names and session names
## if there are multiple sessions for a subject, the session names should be in a list
sub_ses = [["sub1-ID", ["ses1-ID", "ses2-ID"]], # multiple seesions for a subject can be specified in a list [ses1-ID, ses2-ID, ...]
           ["sub2-ID", ["ses1-ID"]],
]


## directories of subjects and sessions for input and output
input_parent = "/path/to/source/"
output_parent = "/path/to/source/"
name_storage_dir = "nii_loraks_recon"   # name of the directory in the output_parent where the reconstructed data will be stored

with_smaps = True # boolean, specifies if sensitivity maps are also reconstructed
                   # each session file MUST have a corresponding sensitivity map file (2x length of t1w_raw, pdw_raw, mtw_raw)
                   # handled so that each specified session in sub_ses is used twice
smaps_per_session = 2 # integer, number of sensitivity maps per session

## specifying names of the actual pdw, t1w, mtw, and ernst .dat files
## Each one has to be a nested list, where the sessions of each subject are specified in a separate list.
pdw_raw = [[  # sub1-ID  
              "filename_smap.dat",   # ses1-ID
              "filename_smap.dat",  # ses1-ID
              "filename_pdw.dat",    # ses1-ID
           ],
           [  # sub1-ID
              "filename_smap.dat",   # ses2-ID
              "filename_smap.dat",  # ses2-ID
              "filename_pdw.dat",    # ses2-ID
           ],
           [  # sub2-ID
              "filename_smap.dat",   # ses1-ID
              "filename_smap.dat",  # ses1-ID
              "filename_pdw.dat",    # ses1-ID
           ]
]
           
t1w_raw = [[  # sub1-ID
              "filename_smap.dat",   # ses1-ID
              "filename_smap.dat",  # ses1-ID
              "filename_t1w.dat",    # ses1-ID
           ],
           [  # sub1-ID
              "filename_smap.dat",   # ses2-ID
              "filename_smap.dat",  # ses2-ID
              "filename_t1w.dat",    # ses2-ID
           ],
           [  # sub2-ID
              "filename_smap.dat",   # ses1-ID
              "filename_smap.dat",  # ses1-ID
              "filename_t1w.dat",    # ses1-ID
           ]
]

mtw_raw = [[  # sub1-ID 
              "filename_smap.dat",   # ses1-ID
              "filename_smap.dat",   # ses1-ID
              "filename_mtw.dat",    # ses1-ID
           ],
           [  # sub1-ID
              "filename_smap.dat",   # ses2-ID
              "filename_smap.dat",  # ses2-ID
              "filename_mtw.dat",    # ses2-ID
           ],
           [  # sub2-ID
              "filename_smap.dat",   # ses1-ID
              "filename_smap.dat",  # ses1-ID
              "filename_mtw.dat",    # ses1-ID
           ]
]

ernst_raw = None