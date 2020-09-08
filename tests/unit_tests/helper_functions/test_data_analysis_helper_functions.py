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

test_gdf = gpd.GeoDataFrame(test_df.copy(),
                            geometry = random_points,
                            crs = "EPSG:4326")
 
test_gdf_diff_crs = gpd.GeoDataFrame(test_df.copy(),
                            geometry = random_points,
                            crs = "EPSG:32633") 

test_gdf_no_crs = gpd.GeoDataFrame(test_df.copy(),
                            geometry = random_points) 

test_gdf_no_geom = gpd.GeoDataFrame(test_df.copy())

test_gdf_list = [test_gdf, test_gdf]
    
#%%     --- other  ---

test_str = "Test"
test_int = 10
test_float = 10.5
test_bool = False
test_list = ["A,B"]
test_dict = {"A":1, "B":2}
test_sample_size_int_correct = 5
test_sample_size_int_wrong = 105

#%% --- Testing ---

#%% --- Test helper function: is_gdf ---

class TestIsGdf(object):
    def test_false_on_nongdf_value_list(self):
        test_argument = test_list
        expected = False
        actual = functions.is_gdf(test_argument)
        error_message = "Expected function to return {}, function returned {}".format(expected, actual)
        assert expected is actual, error_message
    
    def test_false_on_nongdf_value_str(self):
        test_argument = test_str
        expected = False
        actual = functions.is_gdf(test_argument)
        error_message = "Expected function to return {}, function returned {}".format(expected, actual)
        assert expected is actual, error_message
    
    def test_true_on_gdf_value(self):
        test_argument = test_gdf
        expected = True
        actual = functions.is_gdf(test_argument)
        error_message = "Expected function to return {}, function returned {}".format(expected, actual)
        assert expected is actual, error_message

#%% --- Test helper function: test_if_all_elements_are_gdf ---
class TestCheckIfAllElementsAreGdf(object):
    def test_valerror_on_nonlist_value_bool(self):
        test_argumentslist = test_bool
        expected_message = "arguments_list must be of type list. Got {}".format(type(test_argumentslist))
        with pytest.raises(ValueError) as exception_info:
            functions.check_if_all_elements_are_gdf(test_argumentslist)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_valerror_on_nonlist_value_dict(self):
        test_argumentslist = test_dict
        expected_message = "arguments_list must be of type list. Got {}".format(type(test_argumentslist))
        with pytest.raises(ValueError) as exception_info:
            functions.check_if_all_elements_are_gdf(test_argumentslist)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_false_on_nongdf_list(self):
        test_argumentslist = test_list
        expected = False
        actual = functions.check_if_all_elements_are_gdf(test_argumentslist)
        error_message = "Expected function to return {}, function returned {}".format(expected, actual)
        assert expected is actual, error_message
    
    def test_true_on_gdf_list(self):
        test_argumentslist = test_gdf_list
        expected = True
        actual = functions.check_if_all_elements_are_gdf(test_argumentslist)
        error_message = "Expected function to return {}, function returned {}".format(expected, actual)
        assert expected is actual, error_message
    
#%% --- Test helper function: has_crs ---

class TestHasCrs(object):
    def test_valerror_on_nongdf_value_bool(self):
        test_geodataframe = test_bool
        expected_message = "Function arguments should be of type geopandas.GeoDataFrame. Got at least one {} ".format(type(test_geodataframe))
        with pytest.raises(ValueError) as exception_info:
            functions.has_crs(test_geodataframe)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_valerror_on_nongdf_values_str(self):
        test_geodataframe_1 = test_str
        test_geodataframe_2 = test_str
        expected_message = "Function arguments should be of type geopandas.GeoDataFrame. Got at least one {} ".format(type(test_geodataframe_1))
        with pytest.raises(ValueError) as exception_info:
            functions.has_crs(test_geodataframe_1, test_geodataframe_2)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_valerror_on_gdf_and_nongdf_values(self):
        test_geodataframe_1 = test_gdf
        test_geodataframe_2 = test_str
        expected_message = "Function arguments should be of type geopandas.GeoDataFrame. Got at least one {} ".format(type(test_geodataframe_2))
        with pytest.raises(ValueError) as exception_info:
            functions.has_crs(test_geodataframe_1, test_geodataframe_2)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_false_on_no_crs(self):
        test_geodataframe = test_gdf_no_crs
        expected = False
        actual = functions.has_crs(test_geodataframe)
        error_message = "Expected function to return {}, function returned {}".format(expected, actual)
        assert expected is actual, error_message
    
    def test_false_on_no_crs_multiple_values(self):
        test_geodataframe_1 = test_gdf_no_crs
        test_geodataframe_2 = test_gdf
        expected = False
        actual = functions.has_crs(test_geodataframe_1, test_geodataframe_2)
        error_message = "Expected function to return {}, function returned {}".format(expected, actual)
        assert expected is actual, error_message
    
    def test_true_on_crs(self):
        test_geodataframe = test_gdf
        expected = True
        actual = functions.has_crs(test_geodataframe)
        error_message = "Expected function to return {}, function returned {}".format(expected, actual)
        assert expected is actual, error_message
    
    def test_true_on_crs_multiple_values(self):
        test_geodataframe_1 = test_gdf
        test_geodataframe_2 = test_gdf
        expected = True
        actual = functions.has_crs(test_geodataframe_1, test_geodataframe_2)
        error_message = "Expected function to return {}, function returned {}".format(expected, actual)
        assert expected is actual, error_message
        

#%% -- Test helper function: has_geometry ---

class TestHasGeometry(object):
    def test_valerror_on_nongdf_value_float(self):
        test_geodataframe = test_float
        expected_message = "Function arguments should be of type geopandas.GeoDataFrame. Got at least one {} ".format(type(test_geodataframe))
        with pytest.raises(ValueError) as exception_info:
            functions.has_geometry(test_geodataframe)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
        
    def test_valerror_on_nongdf_value_str(self):
        test_geodataframe = test_str
        expected_message = "Function arguments should be of type geopandas.GeoDataFrame. Got at least one {} ".format(type(test_geodataframe))
        with pytest.raises(ValueError) as exception_info:
            functions.has_geometry(test_geodataframe)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
        
    def test_false_on_no_geometry(self):
        test_geodataframe = test_gdf_no_geom
        expected = False
        actual = functions.has_geometry(test_geodataframe)
        error_message = "Expected function to return {}, function returned {}".format(expected, actual)
        assert expected is actual, error_message
    
    def test_true_on_geometry(self):
        test_geodataframe = test_gdf
        expected = True
        actual = functions.has_geometry(test_geodataframe)
        error_message = "Expected function to return {}, function returned {}".format(expected, actual)
        assert expected is actual, error_message
        


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
    
    def test_attriberror_on_missing_crs(self):
        test_geodataframe_1 = test_gdf
        test_geodataframe_2 = test_gdf_no_crs
        expected_message = "At least one geopandas.GeoDataFrame object is missing crs information."
        with pytest.raises(AttributeError) as exception_info:
            functions.crs_is_equal(test_geodataframe_1,test_geodataframe_2)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_false_on_inequal_crs(self):
        test_geodataframe_1 = test_gdf
        test_geodataframe_2 = test_gdf_diff_crs
        expected = False
        actual = functions.crs_is_equal(test_geodataframe_1, test_geodataframe_2)
        error_message = "Expected function to return {}, function returned {}".format(expected, actual)
        assert expected is actual, error_message
        
    
    def test_true_on_equal_crs(self):
        test_geodataframe_1 = test_gdf
        test_geodataframe_2 = test_gdf
        expected = True
        actual = functions.crs_is_equal(test_geodataframe_1, test_geodataframe_2)
        error_message = "Expected function to return {}, function returned {}".format(expected, actual)
        assert expected is actual, error_message
        
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

def TestNearestNeighborAnalysis(object):
    def test_attriberror_on_uneven_crs(self):
        test_geodataframe_1 = test_gdf
        test_geodataframe_2 = test_gdf_diff_crs
        expected_message = ("The arguments provided to do not share the same crs."
                        "Got {} and {} as crs.").format(test_geodataframe_1.crs, test_geodataframe_2.crs)
        with pytest.raises(AttributeError) as exception_info:
            functions.nearest_neighbor_analysis(test_geodataframe_1, test_geodataframe_2)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
        
        
    