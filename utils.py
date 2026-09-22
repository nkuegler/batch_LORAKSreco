def count_session_files(nested_list,length=None):
    for sub in nested_list:
        for ses in sub:
            if not isinstance(ses,list):
                raise ValueError(f"Improper format, nested list is too deep.")
            if length is None:
                length = len(ses)
            elif len(ses) != length:
                raise ValueError(f"Number of sessions files not the same!\nIf this is intended set enforce_same_session_length to False")