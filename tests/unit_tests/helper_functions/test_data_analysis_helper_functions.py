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
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from src.helper_functions import data_analysis_helper_functions as functions

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Create test data ---
#%%     --- Mock DataFrame ---

#Create a random seed
np.random.seed([3,1415])
#Create a dataframe from random np numbers
test_df = pd.DataFrame(np.random.randint(10, size=(100, 5)),
                       columns=list('ABCDE'))
#Select ten percent of each column and turn it into np.nan
for col in test_df.columns:
    test_df.loc[test_df.sample(frac=0.1).index, col] = np.nan
    
#%%     --- Mock GeoDataFrame ---

random_points_basis_x = np.random.randint(low = 20, high = 40, size = 100)
random_points_basis_y = np.random.randint(low = 20, high = 40, size = 100)
random_points = [Point(x,y) for (x,y) in zip(random_points_basis_x,random_points_basis_y)]
test_gdf = gpd.GeoDataFrame(test_df,
                            geometry = random_points,
                            crs = "EPSG:4326") 

test_gdf_no_crs = gpd.GeoDataFrame(test_df,
                            geometry = random_points) 
    
#%%     --- other  ---

test_str = "Test"
test_int = 10
test_float = 10.5
test_bool = False
test_sample_size_int_correct = 5
test_sample_size_int_wrong = 105

#%% --- Testing ---

#%% --- Test helper function: crs_is_equal ---

class TestCrsIsEqual(object):
    def test_valerror_on_nongdf_values_str_and_int(self):
        test_geodataframe_1 = test_str
        test_geodataframe_2 = test_int
        expected_message = ("Both function arguments should be of type geopandas.GeoDataFrame"
        "Got {} and {}").format(type(test_geodataframe_1), type(test_geodataframe_2))
        with pytest.raises(ValueError) as exception_info:
            functions.crs_is_equal(test_geodataframe_1,test_geodataframe_2)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
        
    def test_valerror_on_gdf_and_nongdf_values_int(self):
        test_geodataframe_1 = test_gdf
        test_geodataframe_2 = test_int
        expected_message = ("Both function arguments should be of type geopandas.GeoDataFrame"
        "Got {} and {}").format(type(test_geodataframe_1), type(test_geodataframe_2))
        with pytest.raises(ValueError) as exception_info:
            functions.crs_is_equal(test_geodataframe_1,test_geodataframe_2)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_valerror_on_missing_crs(self):
        test_geodataframe_1 = test_gdf
        test_geodataframe_2 = test_gdf_no_crs
        expected_message = "At least one geopandas.GeoDataFrame object is missing crs information."
        with pytest.raises(ValueError) as exception_info:
            functions.crs_is_equal(test_geodataframe_1,test_geodataframe_2)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
        
            
        
#%% -- Test helper function: has_geometry ---


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
    