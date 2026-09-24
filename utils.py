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