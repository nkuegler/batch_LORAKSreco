#!/usr/bin/env python3
"""
Script to generate a prestructured config file based on sub_ses dictionary.
Creates empty entries for pdw_raw, t1w_raw, mtw_raw, and ernst_raw.
"""

def generate_config_template(sub_ses, with_smaps=True, smaps_per_session=2):
    """
    Generate a prestructured config file based on sub_ses dictionary.
    
    Parameters:
    -----------
    sub_ses : list of lists
        List where each element is [subject_name, [session_names]]
    with_smaps : bool
        Whether sensitivity maps are included (default: True)
    smaps_per_session : int
        Number of sensitivity maps per session (default: 2)
    
    Returns:
    --------
    dict
        Dictionary containing the prestructured config fields
    """
    
    # Initialize the config dictionary
    config = {}
    
    # Copy sub_ses to config
    config['sub_ses'] = sub_ses
    
    # Generate empty entries for each subject
    pdw_raw = []
    t1w_raw = []
    mtw_raw = []
    ernst_raw = []
    
    for subject_info in sub_ses:
        subject_name = subject_info[0]
        sessions = subject_info[1]
        
        # For each session, create empty entries
        for session in sessions:
            # Determine number of entries per session
            if with_smaps:
                num_entries = smaps_per_session + 1  # smaps + actual data
            else:
                num_entries = 1  # just the actual data
            
            # Create empty entries for this session
            session_entries = ['""'] * num_entries
            
            # Add to each modality list
            pdw_raw.append(session_entries)
            t1w_raw.append(session_entries)
            mtw_raw.append(session_entries)
            ernst_raw.append(session_entries)
    
    config['pdw_raw'] = pdw_raw
    config['t1w_raw'] = t1w_raw
    config['mtw_raw'] = mtw_raw
    config['ernst_raw'] = ernst_raw
    
    return config


def write_config_to_file(config, output_filename):
    """
    Write the config dictionary to a Python file.
    
    Parameters:
    -----------
    config : dict
        Dictionary containing the config fields
    output_filename : str
        Name of the output file
    """
    
    with open(output_filename, 'w') as f:
        # Write header
        f.write("#!/usr/bin/env python3\n\n")
        f.write("## Auto-generated config file\n")
        f.write("## Generated from sub_ses dictionary\n\n")
        
        # Write sub_ses
        f.write("## subject names and session names\n")
        f.write("## if there are multiple sessions for a subject, the session names should be in a list\n")
        f.write("sub_ses = ")
        f.write(str(config['sub_ses']))
        f.write("\n\n")
        
        # Write directories (placeholders)
        f.write("## directories of subjects and sessions for input and output\n")
        f.write('input_parent = "/path/to/input/"\n')
        f.write('output_parent = "/path/to/output/"\n')
        f.write('name_storage_dir = "nii_loraks_recon"\n\n')
        
        f.write("with_smaps = True\n")
        f.write("smaps_per_session = 2\n\n")
        
        # Write pdw_raw
        f.write("## specifying names of the actual pdw .dat files\n")
        f.write("pdw_raw = ")
        f.write(format_nested_list(config['pdw_raw'], config['sub_ses']))
        f.write("\n\n")
        
        # Write t1w_raw
        f.write("## specifying names of the actual t1w .dat files\n")
        f.write("t1w_raw = ")
        f.write(format_nested_list(config['t1w_raw'], config['sub_ses']))
        f.write("\n\n")
        
        # Write mtw_raw
        f.write("## specifying names of the actual mtw .dat files\n")
        f.write("mtw_raw = ")
        f.write(format_nested_list(config['mtw_raw'], config['sub_ses']))
        f.write("\n\n")
        
        # Write ernst_raw
        f.write("## specifying names of the actual ernst .dat files\n")
        f.write("ernst_raw = ")
        f.write(format_nested_list(config['ernst_raw'], config['sub_ses']))
        f.write("\n\n")
    
    print(f"Config file written to: {output_filename}")


def format_nested_list(nested_list, sub_ses):
    """
    Format a nested list with comments for subject and session names.
    
    Parameters:
    -----------
    nested_list : list
        The nested list to format
    sub_ses : list
        The sub_ses list for subject and session names
    
    Returns:
    --------
    str
        Formatted string representation
    """
    
    result = "[\n"
    
    session_idx = 0
    for subject_info in sub_ses:
        subject_name = subject_info[0]
        sessions = subject_info[1]
        
        for session in sessions:
            # Add subject comment
            result += f"           [  # {subject_name}\n"
            
            # Add session comment and entries
            entries = nested_list[session_idx]
            for entry in entries:
                result += f'              {entry},  # {session}\n'
            
            result += "           ],\n"
            session_idx += 1
    
    result += "]"
    return result


def main():
    """
    Main function to demonstrate usage.
    """
    
    # Example sub_ses dictionary (modify as needed)
    sub_ses = [["35028.02", ["20260702"]],
            ["44068.e7", ["20260707"]],
            ["30816.8c", ["20260709"]],
            ["13719.18", ["20260714"]],
            ["38829.2f", ["20260707"]],
            ["04364.c6", ["20260707"]],
            ["44568.68", ["20260728"]],
            ["35076.16", ["20260723"]],
            ["08950.3f", ["20260804"]],
    ]
    
    # Generate config template
    config = generate_config_template(sub_ses)
    
    # Write to file
    output_filename = "config_template.py"
    write_config_to_file(config, output_filename)
    
    print("\nGenerated config structure:")
    print(f"  Subjects: {len(sub_ses)}")
    print(f"  Total sessions: {sum(len(s[1]) for s in sub_ses)}")
    print(f"  Entries per session: {len(config['pdw_raw'][0])}")


if __name__ == "__main__":
    main()