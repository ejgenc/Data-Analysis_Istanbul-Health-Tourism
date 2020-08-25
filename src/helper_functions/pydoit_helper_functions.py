# -*- coding: utf-8 -*-
"""
------ What is this file? ------

This script contains some helper functions that are used in all the scripts.
The scripts mainly serve to resolve issues that arise when using the pydoit build automation tool.
The unit tests for these functions can be found at:
     tests/unit_tests/helper_functions/test_pydoit_helper_functions.py

"""

#%% --- Import required packages ---
import os
import pathlib
from pathlib import Path # To wrap around filepaths


def resolve_path(path, root_directory_name):
    internal_path = path
    
    dirname = os.path.dirname(__file__)
    dirname_split = dirname.split("\\")
    
    if dirname_split[0] == root_directory_name:
        internal_path_split = internal_path.split("/")
        internal_path_split[:] = [segment for segment in internal_path_split if segment != ".."]
        # for segment in internal_path_split:
        #     if segment == "..":
        #         internal_path_split.remove(segment)
                
        seperator = "/"
        internal_path = seperator.join(internal_path_split)
        
    return Path(internal_path)




    
    
    

