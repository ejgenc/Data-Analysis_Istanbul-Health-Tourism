# -*- coding: utf-8 -*-
"""
------ What is this file? ------

This test module contains some tests for the data_analysis_visualization_functions.py script.
The script can be found at:
    src/helper_functions/data_visualization_helper_functions.py

"""
#%% --- Import Required Packages ---

import os
import pytest
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon, MultiPoint
from src.helper_functions import data_analysis_helper_functions as functions_analysis
from src.helper_functions import data_visualization_helper_functions as functions_visualization

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

#%% --- Test figure ---

test_fig = plt.figure()
ax = test_fig.add_subplot(1,1,1)
ax.scatter(test_df["A"], test_df["B"])
#%% --- Testing ---

#%% --- Test subfunction: create_link_between_origin_and_nearest_geom ---

class TestCreateLinkBetweenOriginAndNearestGeom(object):
    def test_valerror_on_nongdf_argument_str(self):
        test_geodataframe = test_str
        expected_message = "Argument nn_analysis_gdf should be of type geopandas.GeoDataFrame. Got {} ".format(type(test_geodataframe))
        with pytest.raises(ValueError) as exception_info:
            functions_visualization.create_link_between_origin_and_nearest_geom(test_geodataframe)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_attriberror_on_missing_geometry(self):
        test_geodataframe = test_gdf_no_geom
        expected_message = "Argument provided does not have geometry information."
        with pytest.raises(AttributeError) as exception_info:
            functions_visualization.create_link_between_origin_and_nearest_geom(test_geodataframe)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
        
    def test_attriberror_on_missing_crs(self):
        test_geodataframe= test_gdf_no_crs
        expected_message = "nn_analysis_gdf object is missing crs information."
        with pytest.raises(AttributeError) as exception_info:
            functions_visualization.create_link_between_origin_and_nearest_geom(test_geodataframe)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
#%% --- Test subfunction: plot_nearest_neighbor_analysis ---

class TestPlotNearestNeighborAnalysis(object):
    def test_valerror_on_nongdf_argument_bool(self):
        test_geodataframe = test_bool
        expected_message = "Argument nn_analysis_gdf should be of type geopandas.GeoDataFrame. Got {} ".format(type(test_geodataframe))
        with pytest.raises(ValueError) as exception_info:
            functions_visualization.plot_nearest_neighbor_analysis(test_geodataframe, test_gseries)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_attriberror_on_missing_geometry(self):
        test_geodataframe = test_gdf_no_geom
        expected_message = "Argument provided does not have geometry information."
        with pytest.raises(AttributeError) as exception_info:
            functions_visualization.plot_nearest_neighbor_analysis(test_geodataframe, test_gseries)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_attriberror_on_missing_crs(self):
        test_geodataframe= test_gdf_no_crs
        expected_message = "nn_analysis_gdf object is missing crs information."
        with pytest.raises(AttributeError) as exception_info:
            functions_visualization.plot_nearest_neighbor_analysis(test_geodataframe, test_gseries)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
#%% --- Test main function: confirm_nearest_neighbor_analysis ---

class TestConfirmNearestNeighborAnalysis(object):
    def test_valerror_on_nongdf_argument_df(self):
        test_geodataframe = test_df
        expected_message = "Argument nn_analysis_gdf should be of type geopandas.GeoDataFrame. Got {} ".format(type(test_geodataframe))
        with pytest.raises(ValueError) as exception_info:
            functions_visualization.confirm_nearest_neighbor_analysis(test_geodataframe)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_attriberror_on_missing_geometry(self):
        test_geodataframe = test_gdf_no_geom
        expected_message = "Argument provided does not have geometry information."
        with pytest.raises(AttributeError) as exception_info:
            functions_visualization.confirm_nearest_neighbor_analysis(test_geodataframe)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
        
#%% --- Test main function: add_watermark ---

class TestAddWatermark(object):
    def test_valerror_on_nonplt_plt(self):
        test_plt = test_int
        expected_message = "Argument fig should be of type matplotlib.Figure. Got {} ".format(type(test_plt))
        with pytest.raises(ValueError) as exception_info:
            functions_visualization.add_watermark(test_plt, "Test")
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_valerror_on_nonstr_watermark(self):
        test_watermark = test_bool
        expected_message = "Argument watermark_str should be of type str. Got {} ".format(type(test_watermark))
        with pytest.raises(ValueError) as exception_info:
            functions_visualization.add_watermark(test_fig, test_watermark)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    


