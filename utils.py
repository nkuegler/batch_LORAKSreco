import tempfile
import json

def is_raw_valid(nested_list: list, enforce_same_length:bool):
    """
    Ensures the raw nested lists are correctly structured,
    correct structed is a 3-layer deep nested list
    """
    length = None
    for sub in nested_list:
        for ses in sub:
            if not isinstance(ses,list):
                raise ValueError(f"Improper format: nested list is too deep.")
            
            if enforce_same_length:
                if length is None:
                    length = len(ses)
                elif len(ses) != length:
                    raise ValueError(
                        "Number of session files is not uniform across sessions\n"
                        "Set enforce_same_length=False to disable this check."
                    )

def count_longest_session(nested_list: list, length) -> int:
    """finds the longest session length in nested list updates length"""
    if length == None:
        length = 0
    max_in_session = max((len(ses) for sub in nested_list for ses in sub), default=0)
    return max_in_session if max_in_session > length else length

def loraks_config(input_path:str,config_main:dict,smap_strings:list=['smaps','sens']):
    """
    This function uses the input_path to determine whether the sbatch command
    input file is a sensitivity map or not. Then builds the appropriate json config
    as a tempfile returns the file path of that temp file 
    for use in reconstruction(..., config).

    The temp json file is cleaned up by recon.sh via 'rm $4'
    """
    if not input_path:
        # unnecessary safety check
        return None 

    # copy config_main
    config_dict = config_main.copy()

    if any(term in input_path for term in smap_strings):
        config_dict['loraksConfig'] = config_dict['smap_adjustments']['loraksConfig']

    config_dict.pop('smap_adjustments')

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json',delete=False) as config:
        json.dump(config_dict, config, indent=2)
    return config.name