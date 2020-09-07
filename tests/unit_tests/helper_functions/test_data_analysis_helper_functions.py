# -*- coding: utf-8 -*-
"""
------ What is this file? ------

This test module contains some tests for the data_analysis_helper_functions.py script.
The script can be found at:
    src/helper_functions/data_analysis_helper_functions.py

"""

#%% --- Import Required Packages ---

import os
from pathlib import Path # To wrap around filepaths
import pytest
import geopandas as gpd
from src.helper_functions import data_analysis_helper_functions as functions

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


#%% --- Create test data ---

    #%% --- Mock GeoDataFrame ---

    #%% --- other  ---

test_str = "Test"
test_int = 10
test_float = 10.5
test_bool = False
test_sample_size_int_correct = 5
test_sample_size_int_wrong = 105

#%% --- Testing ---

#%%     --- Test subfuction: calculate_centroid

class TestCalculateCentroid(object):
    def test_valerror_on_nongdf_value_bool(self):
        pass
    
    def test_valerror_on_nongdf_value_int(self):
        pass

#%%     --- Test subfunction: create_unary_union

#%%     --- Test subfunction: calculate_nearest_neighbor

#%%     --- Test subfunction: calculate_distance

#%%     --- Test main function: nearest_neighbor_analysis
    