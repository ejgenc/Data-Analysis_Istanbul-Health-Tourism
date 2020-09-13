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
from shapely.geometry import Point, Polygon, MultiPoint
from shapely.ops import nearest_points
from geopy import distance
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
sample_polygon = Polygon([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]])
sample_polygons = [sample_polygon for i in range (0,100)]

test_gdf = gpd.GeoDataFrame(test_df.copy(),
                            geometry = random_points,
                            crs = "EPSG:4326")

test_gseries = gpd.GeoSeries(random_points,
                             crs = "EPSG:4326")
 
test_gdf_diff_crs = gpd.GeoDataFrame(test_df.copy(),
                            geometry = random_points,
                            crs = "EPSG:32633") 

test_gdf_no_crs = gpd.GeoDataFrame(test_df.copy(),
                            geometry = random_points) 

test_gdf_no_geom = gpd.GeoDataFrame(test_df.copy())

test_gdf_geom_is_polygon = gpd.GeoDataFrame(test_df.copy(),
                            geometry = sample_polygons,
                            crs = "EPSG:4326")

test_gdf_list = [test_gdf, test_gdf]

test_multipoint_object = test_gdf.geometry.unary_union

test_nearest_point_gdf = test_gdf.rename(columns = {"A" : "point_of_origin",
                                                    "B" : "nearest_point"})

    
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
    def test_valerror_on_nongdf_value_df(self):
        test_geodataframe = test_df
        expected_message = "Function argument should be of type geopandas.GeoDataFrame. Got {}".format(type(test_geodataframe))
        with pytest.raises(ValueError) as exception_info:
            functions.has_crs(test_geodataframe)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
        
    def test_valerror_on_nongdf_value_list(self):
        test_geodataframe = test_list
        expected_message = "Function argument should be of type geopandas.GeoDataFrame. Got {}".format(type(test_geodataframe))
        with pytest.raises(ValueError) as exception_info:
            functions.has_crs(test_geodataframe)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_false_on_no_crs(self):
        test_geodataframe = test_gdf_no_crs
        expected = False
        actual = functions.has_crs(test_geodataframe)
        error_message = "Expected function to return {}, function returned {}".format(expected, actual)
        assert expected is actual, error_message
    
    def test_true_on_crs(self):
        test_geodataframe = test_gdf
        expected = True
        actual = functions.has_crs(test_geodataframe)
        error_message = "Expected function to return {}, function returned {}".format(expected, actual)
        assert expected is actual, error_message
            
#%% --- Test helper function: check_if_all_elements_have_crs ---

class TestCheckIfAllElementsHaveCrs(object):
    def test_valerror_on_nonlist_value_dict(self):
        test_geodataframes_list = test_dict
        expected_message = "geodataframes_list must be of list type. Got {}".format(type(test_geodataframes_list))
        with pytest.raises(ValueError) as exception_info:
            functions.check_if_all_elements_have_crs(test_geodataframes_list)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_valerror_on_nonlist_value_df(self):
        test_geodataframes_list = test_df
        expected_message = "geodataframes_list must be of list type. Got {}".format(type(test_geodataframes_list))
        with pytest.raises(ValueError) as exception_info:
            functions.check_if_all_elements_have_crs(test_geodataframes_list)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_valerror_on_nongdf_list_elements_str(self):
        test_geodataframe_1 = test_str
        test_geodataframe_2 = test_str
        test_list = [test_geodataframe_1, test_geodataframe_2]
        expected_message = "Elements of the list should be of type geopandas.GeoDataFrame. Got at least one value that is not."
        with pytest.raises(ValueError) as exception_info:
            functions.check_if_all_elements_have_crs(test_list)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_valerror_on_gdf_and_nongdf_list_elements(self):
        test_geodataframe_1 = test_gdf
        test_geodataframe_2 = test_str
        test_list = [test_geodataframe_1, test_geodataframe_2]
        expected_message = "Elements of the list should be of type geopandas.GeoDataFrame. Got at least one value that is not."
        with pytest.raises(ValueError) as exception_info:
            functions.check_if_all_elements_have_crs(test_list)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
        
    def test_false_on_no_crs_multiple_list_elements(self):
        test_geodataframe_1 = test_gdf_no_crs
        test_geodataframe_2 = test_gdf
        test_list = [test_geodataframe_1, test_geodataframe_2]
        expected = False
        actual = functions.check_if_all_elements_have_crs(test_list)
        error_message = "Expected function to return {}, function returned {}".format(expected, actual)
        assert expected is actual, error_message
        
    def test_true_on_crs_multiple_list_elements(self):
        test_geodataframe_1 = test_gdf
        test_geodataframe_2 = test_gdf
        test_list = [test_geodataframe_1, test_geodataframe_2]
        expected = True
        actual = functions.check_if_all_elements_have_crs(test_list)
        error_message = "Expected function to return {}, function returned {}".format(expected, actual)
        assert expected is actual, error_message
        

#%% -- Test helper function: has_geometry ---

class TestHasGeometry(object):
    def test_valerror_on_nongdf_value_float(self):
        test_geodataframe = test_float
        expected_message = "Function argument should be of type geopandas.GeoDataFrame. Got {} ".format(type(test_geodataframe))
        with pytest.raises(ValueError) as exception_info:
            functions.has_geometry(test_geodataframe)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
        
    def test_valerror_on_nongdf_value_str(self):
        test_geodataframe = test_str
        expected_message = "Function argument should be of type geopandas.GeoDataFrame. Got {} ".format(type(test_geodataframe))
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
        
#%% --- Test helper function: check_if_all_elements_have_geometry ---

class TestCheckIfAllElementsHaveGeometry(object):
    def test_valerror_on_nonlist_value_dict(self):
        test_geodataframes_list = test_dict
        expected_message = "geodataframes_list must be of list type. Got {}".format(type(test_geodataframes_list))
        with pytest.raises(ValueError) as exception_info:
            functions.check_if_all_elements_have_geometry(test_geodataframes_list)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_valerror_on_nonlist_value_df(self):
        test_geodataframes_list = test_df
        expected_message = "geodataframes_list must be of list type. Got {}".format(type(test_geodataframes_list))
        with pytest.raises(ValueError) as exception_info:
            functions.check_if_all_elements_have_geometry(test_geodataframes_list)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_valerror_on_nongdf_list_elements_str(self):
        test_geodataframe_1 = test_str
        test_geodataframe_2 = test_str
        test_list = [test_geodataframe_1, test_geodataframe_2]
        expected_message = "Elements of the list should be of type geopandas.GeoDataFrame. Got at least one value that is not."
        with pytest.raises(ValueError) as exception_info:
            functions.check_if_all_elements_have_geometry(test_list)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_valerror_on_gdf_and_nongdf_list_elements(self):
        test_geodataframe_1 = test_gdf
        test_geodataframe_2 = test_str
        test_list = [test_geodataframe_1, test_geodataframe_2]
        expected_message = "Elements of the list should be of type geopandas.GeoDataFrame. Got at least one value that is not."
        with pytest.raises(ValueError) as exception_info:
            functions.check_if_all_elements_have_geometry(test_list)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
        
    def test_false_on_no_geom_multiple_list_elements(self):
        test_geodataframe_1 = test_gdf_no_geom
        test_geodataframe_2 = test_gdf
        test_list = [test_geodataframe_1, test_geodataframe_2]
        expected = False
        actual = functions.check_if_all_elements_have_geometry(test_list)
        error_message = "Expected function to return {}, function returned {}".format(expected, actual)
        assert expected is actual, error_message
        
    def test_true_on_gdf_multiple_list_elements(self):
        test_geodataframe_1 = test_gdf
        test_geodataframe_2 = test_gdf
        test_list = [test_geodataframe_1, test_geodataframe_2]
        expected = True
        actual = functions.check_if_all_elements_have_geometry(test_list)
        error_message = "Expected function to return {}, function returned {}".format(expected, actual)
        assert expected is actual, error_message

#%% --- Test helper function: crs_is_equal ---

class TestCrsIsEqual(object):
    def test_valerror_on_nongdf_values_str_and_int(self):
        test_geodataframe_1 = test_str
        test_geodataframe_2 = test_int
        expected_message = "Both function arguments should be of type geopandas.GeoDataFrame"
        with pytest.raises(ValueError) as exception_info:
            functions.crs_is_equal(test_geodataframe_1,test_geodataframe_2)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
        
    def test_valerror_on_gdf_and_nongdf_values_int(self):
        test_geodataframe_1 = test_gdf
        test_geodataframe_2 = test_int
        expected_message = "Both function arguments should be of type geopandas.GeoDataFrame"
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
        
#%% --- Test helper function: map_geometry_types: ---

class TestMapGeometryTypes(object):
    def test_valerror_on_nongdf_value_float(self):
        test_geodataframe = test_float
        expected_message = "Argument provided should be of type geopandas.GeoDataFrame. Got {} ".format(type(test_geodataframe))
        with pytest.raises(ValueError) as exception_info:
            functions.map_geometry_types(test_geodataframe, return_most_common = False)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_valerror_on_nongdf_value_dict(self):
        test_geodataframe = test_dict
        expected_message = "Argument provided should be of type geopandas.GeoDataFrame. Got {} ".format(type(test_geodataframe))
        with pytest.raises(ValueError) as exception_info:
            functions.map_geometry_types(test_geodataframe, return_most_common = False)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_attriberror_on_missing_geometry(self):
        test_geodataframe = test_gdf_no_geom
        expected_message = "Argument provided does not have geometry information."
        with pytest.raises(AttributeError) as exception_info:
            functions.map_geometry_types(test_geodataframe, return_most_common = False)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_valerror_on_incorrect_keyword_arg_str(self):
        test_geodataframe = test_gdf
        expected_message = "Only Boolean True/False can be passed as an argument to return_most_common"
        with pytest.raises(ValueError) as exception_info:
            functions.map_geometry_types(test_geodataframe, return_most_common = "False")
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_output_type_for_return_most_common_false(self):
        test_geodataframe = test_gdf
        expected = pd.Series
        actual = type(functions.map_geometry_types(test_geodataframe, return_most_common = False))
        error_message = "Expected function to return {}, function returned {}".format(expected, actual)
        assert expected is actual, error_message
        
    def test_output_type_for_return_most_common_true(self):
        test_geodataframe = test_gdf
        expected = tuple
        actual = type(functions.map_geometry_types(test_geodataframe, return_most_common = True))
        error_message = "Expected function to return {}, function returned {}".format(expected, actual)
        assert expected is actual, error_message
        
#%%     --- Test subfuction: calculate_centroid --- 

class TestCalculateCentroid(object):
    def test_valerror_on_nongdf_value_bool(self):
        test_geodataframe = test_bool
        expected_message = "Argument provided should be of type geopandas.GeoDataFrame. Got {} ".format(type(test_geodataframe))
        with pytest.raises(ValueError) as exception_info:
            functions.calculate_centroid(test_geodataframe)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_valerror_on_nongdf_value_int(self):
        test_geodataframe = test_int
        expected_message = "Argument provided should be of type geopandas.GeoDataFrame. Got {} ".format(type(test_geodataframe))
        with pytest.raises(ValueError) as exception_info:
            functions.calculate_centroid(test_geodataframe)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_attriberror_on_missing_geometry(self):
        test_geodataframe = test_gdf_no_geom
        expected_message = "Argument provided does not have geometry information."
        with pytest.raises(AttributeError) as exception_info:
            functions.calculate_centroid(test_geodataframe)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_data_type_of_output(self):
        test_geodataframe = test_gdf
        expected = Point
        actual = type(functions.calculate_centroid(test_geodataframe).geometry[0])
        error_message = "Expected function to return {}, function returned {}".format(expected, actual)
        assert expected is actual, error_message
        
#%%     --- Test subfunction: create_unary_union

class TestCreateUnaryUnion(object):
    def test_valerror_on_nongdf_value_dict(self):
        test_geodataframe = test_dict
        expected_message = "Argument provided should be of type geopandas.GeoDataFrame. Got {} ".format(type(test_geodataframe))
        with pytest.raises(ValueError) as exception_info:
            functions.create_unary_union(test_geodataframe)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_valerror_on_nongdf_value_str(self):
        test_geodataframe = test_str
        expected_message = "Argument provided should be of type geopandas.GeoDataFrame. Got {} ".format(type(test_geodataframe))
        with pytest.raises(ValueError) as exception_info:
            functions.create_unary_union(test_geodataframe)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_attriberror_on_missing_geometry(self):
        test_geodataframe = test_gdf_no_geom
        expected_message = "Argument provided does not have geometry information."
        with pytest.raises(AttributeError) as exception_info:
            functions.create_unary_union(test_geodataframe)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
        
    def test_attriberror_on_nonpoint_geometry(self):
        test_geodataframe = test_gdf_geom_is_polygon
        expected_message = ("Geometry information of the argument provided should be composed of Points."
                            "Found at least one non-point shape.")
        with pytest.raises(AttributeError) as exception_info:
            functions.create_unary_union(test_geodataframe)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_data_type_of_output(self):
        test_geodataframe = test_gdf
        expected = MultiPoint
        actual = type(functions.create_unary_union(test_geodataframe))
        error_message = "Expected function to return {}, function returned {}".format(expected, actual)
        assert expected is actual, error_message
        
#%%     --- Test subfunction: prepare_for_nearest_neighbor_analysis ---

class TestPrepareForNearestNeighborAnalysis(object):
    def test_valerror_on_nongdf_value_list(self):
        test_geodataframe = test_list
        expected_message = "Argument provided should be of type geopandas.GeoDataFrame. Got {} ".format(type(test_geodataframe))
        with pytest.raises(ValueError) as exception_info:
            functions.prepare_for_nearest_neighbor_analysis(test_geodataframe)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_valerror_on_nongdf_value_str(self):
        test_geodataframe = test_bool
        expected_message = "Argument provided should be of type geopandas.GeoDataFrame. Got {} ".format(type(test_geodataframe))
        with pytest.raises(ValueError) as exception_info:
            functions.prepare_for_nearest_neighbor_analysis(test_geodataframe)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_attriberror_on_missing_geometry(self):
        test_geodataframe = test_gdf_no_geom
        expected_message = "Argument provided does not have geometry information."
        with pytest.raises(AttributeError) as exception_info:
            functions.prepare_for_nearest_neighbor_analysis(test_geodataframe)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
        
    def test_attriberror_on_nonpoint_geometry(self):
        test_geodataframe = test_gdf_geom_is_polygon
        expected_message = ("Geometry information of the argument provided should be composed of Points."
                            "Found at least one non-point shape.")
        with pytest.raises(AttributeError) as exception_info:
            functions.prepare_for_nearest_neighbor_analysis(test_geodataframe)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_data_type_of_output(self):
        test_geodataframe = test_gdf
        expected = MultiPoint
        actual = type(functions.prepare_for_nearest_neighbor_analysis(test_geodataframe))
        error_message = "Expected function to return {}, function returned {}".format(expected, actual)
        assert expected is actual, error_message

#%%     --- Test subfunction: calculate_nearest_neighbor

class TestCalculateNearestNeighbor(object):
    def test_valerror_on_nongdf_value_bool(self):
        test_geodataframe = test_bool
        test_multipoint_obj = test_multipoint_object
        expected_message = "Argument geodataframe should be of type geopandas.GeoDataFrame. Got {} ".format(type(test_geodataframe))
        with pytest.raises(ValueError) as exception_info:
            functions.calculate_nearest_neighbor(test_geodataframe, test_multipoint_obj)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_valerror_on_nongdf_value_df(self):
        test_geodataframe = test_df
        test_multipoint_obj = test_multipoint_object
        expected_message = "Argument geodataframe should be of type geopandas.GeoDataFrame. Got {} ".format(type(test_geodataframe))
        with pytest.raises(ValueError) as exception_info:
            functions.calculate_nearest_neighbor(test_geodataframe, test_multipoint_obj)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_valerror_on_nonmultipoint_value_str(self):
        test_geodataframe = test_gdf
        test_multipoint_obj = test_str
        expected_message = "Argument multipoint_obj should be of type shapely.geometry.MultiPoint. Got {} ".format(type(test_multipoint_obj))
        with pytest.raises(ValueError) as exception_info:
            functions.calculate_nearest_neighbor(test_geodataframe, test_multipoint_obj)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_valerror_on_nonmultipoint_value_int(self):
        test_geodataframe = test_gdf
        test_multipoint_obj = test_int
        expected_message = "Argument multipoint_obj should be of type shapely.geometry.MultiPoint. Got {} ".format(type(test_multipoint_obj))
        with pytest.raises(ValueError) as exception_info:
            functions.calculate_nearest_neighbor(test_geodataframe, test_multipoint_obj)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_valerror_on_nongdf_nonmultipoint_values(self):
        test_geodataframe = test_df
        test_multipoint_obj = test_int
        expected_message = "Argument geodataframe should be of type geopandas.GeoDataFrame. Got {} ".format(type(test_geodataframe))
        with pytest.raises(ValueError) as exception_info:
            functions.calculate_nearest_neighbor(test_geodataframe, test_multipoint_obj)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_attriberror_on_missing_geometry(self):
        test_geodataframe = test_gdf_no_geom
        test_multipoint_obj = test_multipoint_object
        expected_message = "Argument provided does not have geometry information."
        with pytest.raises(AttributeError) as exception_info:
            functions.calculate_nearest_neighbor(test_geodataframe, test_multipoint_obj)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_attriberror_on_nonpoint_geometry(self):
        test_geodataframe = test_gdf_geom_is_polygon
        test_multipoint_obj = test_multipoint_object
        expected_message = ("Geometry information of the argument provided should be composed of Points."
                            "Found at least one non-point shape.")
        with pytest.raises(AttributeError) as exception_info:
            functions.calculate_nearest_neighbor(test_geodataframe, test_multipoint_obj)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_data_type_of_output(self):
        test_geodataframe = test_gdf
        test_multipoint_obj = test_multipoint_object
        expected = gpd.geodataframe.GeoDataFrame
        actual = type(functions.calculate_nearest_neighbor(test_geodataframe, test_multipoint_obj))
        error_message = "Expected function to return {}, function returned {}".format(expected, actual)
        assert expected is actual, error_message
        
    
    def test_crs_equality_of_output(self):
        test_geodataframe = test_gdf
        test_multipoint_obj = test_multipoint_object
        expected = test_geodataframe.crs
        actual = functions.calculate_nearest_neighbor(test_geodataframe, test_multipoint_obj).crs
        error_message = "Expected output geoDataFrame crs to be {} but crs is {}".format(expected, actual)
        assert expected is actual, error_message
        
    
    def test_geometry_equality_of_output(self):
        test_geodataframe = test_gdf
        test_multipoint_obj = test_multipoint_object
        expected = len(test_geodataframe.geometry)
        actual = test_geodataframe.geometry.geom_equals(functions.calculate_nearest_neighbor(test_geodataframe, test_multipoint_obj).geometry).sum()
        error_message = "Expected output geoDataFrame crs to be {} but crs is {}".format(expected, actual)
        assert int(expected) is int(actual), error_message
    
#%%     --- Test subfunction: calculate_distance

class TestCalculateDistance(object):
    def test_valerror_on_nongdf_value_str(self):
        test_geodataframe = test_str
        expected_message = "Argument nearest_points_gdf should be of type geopandas.GeoDataFrame. Got {} ".format(type(test_geodataframe))
        with pytest.raises(ValueError) as exception_info:
            functions.calculate_distance(test_geodataframe)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_valerror_on_nongdf_value_dict(self):
        test_geodataframe = test_dict
        expected_message = "Argument nearest_points_gdf should be of type geopandas.GeoDataFrame. Got {} ".format(type(test_geodataframe))
        with pytest.raises(ValueError) as exception_info:
            functions.calculate_distance(test_geodataframe)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message

    def test_valerror_on_non_nearest_point_gdf(self):
        test_geodataframe = test_gdf
        expected_message = "The geodataframe provided does not contain columns point_of_origin and nearest_point"
        with pytest.raises(ValueError) as exception_info:
            functions.calculate_distance(test_geodataframe)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
        
#%%     --- Test main function: nearest_neighbor_analysis

@pytest.mark.skip(reason="not fully implemented yet")
class TestNearestNeighborAnalysis(object):
    def test_valerror_on_nongdf_argument_str(self):
        test_gdf_1 = test_str
        test_gdf_2 = test_str
        expected_message = ("Both arguments should be geopandas.GeoDataFrame objects."
                      "Got {} and {} as object types.").format(type(test_gdf_1), type(test_gdf_2))
        with pytest.raises(ValueError) as exception_info:
            functions.nearest_neighbor_analysis(test_gdf_1, test_gdf_2)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_valerror_on_nongdf_arguments_str_and_int(self):
        test_gdf_1 = test_str
        test_gdf_2 = test_int
        expected_message = ("Both arguments should be geopandas.GeoDataFrame objects."
                      "Got {} and {} as object types.").format(type(test_gdf_1), type(test_gdf_2))
        with pytest.raises(ValueError) as exception_info:
            functions.nearest_neighbor_analysis(test_gdf_1, test_gdf_2)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_valerror_on_mixed_arguments_gdf_and_df(self):
        test_gdf_1 = test_gdf
        test_gdf_2 = test_df
        expected_message = ("Both arguments should be geopandas.GeoDataFrame objects."
                      "Got {} and {} as object types.").format(type(test_gdf_1), type(test_gdf_2))
        with pytest.raises(ValueError) as exception_info:
            functions.nearest_neighbor_analysis(test_gdf_1, test_gdf_2)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_attriberror_on_missing_geometry(self):
        test_gdf_1 = test_gdf_no_geom
        test_gdf_2 = test_gdf
        expected_message = "At least one of the arguments provided do not have geometry information."
        with pytest.raises(AttributeError) as exception_info:
            functions.nearest_neighbor_analysis(test_gdf_1, test_gdf_2)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
        
    def test_attriberror_on_missing_geometries(self):
        test_gdf_1 = test_gdf_no_geom
        test_gdf_2 = test_gdf_no_geom
        expected_message = "At least one of the arguments provided do not have geometry information."
        with pytest.raises(AttributeError) as exception_info:
            functions.nearest_neighbor_analysis(test_gdf_1, test_gdf_2)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_attriberror_on_uneven_crs(self):
        test_geodataframe_1 = test_gdf
        test_geodataframe_2 = test_gdf_diff_crs
        expected_message = ("The arguments provided to do not share the same crs."
                        "Got {} and {} as crs.").format(test_geodataframe_1.crs, test_geodataframe_2.crs)
        with pytest.raises(AttributeError) as exception_info:
            functions.nearest_neighbor_analysis(test_geodataframe_1, test_geodataframe_2)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
            
        
#%% =

a = functions.prepare_for_nearest_neighbor_analysis(test_gdf)
b = functions.calculate_nearest_neighbor(test_gdf,a)
c = functions.calculate_distance(b)

    