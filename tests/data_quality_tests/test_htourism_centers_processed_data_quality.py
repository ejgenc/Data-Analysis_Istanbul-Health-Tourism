# -*- coding: utf-8 -*-
"""
------ What is this file? ------

This test module contains some data quality tests for the htourism_centers_processed.shp file.
The file can be found at:
    data/processed/htourism_centers_processed.shp

"""
#%% --- Import Required Packages ---

import os
from pathlib import Path # To wrap around filepaths
import pytest
import numpy as np
import pandas as pd
import geopandas as gpd
import textdistance

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Import data ---

# Dataset to test for quality
import_fp = Path("../../data/processed/htourism_centers_processed.shp")
htourism = gpd.read_file(import_fp, encoding = "utf-8-sig")

# Dataset to take as reference for lat/lon boundaries
import_fp = Path("../../data/external/istanbul_districts.shp")
istanbul_districts = gpd.read_file(import_fp)

#%% --- Data quality tests ---

class TestNullValues(object):
    def test_total_null_values(self):
        expected = 0
        actual = htourism.isnull().sum().sum()
        error_message = "Dataset contains null values. Expected {} null values, got {}".format(expected,actual)
        assert expected == actual, error_message
        
class TestUniqueness(object):
    def test_total_unique_values_for_column_listing_id(self):
        expected = htourism.shape[0]
        actual = len(htourism.loc[:,"institutio"].unique())
        error_message = "Column institutio contains non-unique values. Expected {} unique values, got {}".format(expected, actual)
        assert expected == actual, error_message
        
class TestOutliers(object):
    expected_polygons = istanbul_districts.geometry
    expected_boundaries = expected_polygons.total_bounds
        
    def test_latitude_boundary_min(self):
        expected = self.expected_boundaries[1]
        actual = htourism["latitude"].min()
        error_message = "At least one point is smaller than the minimum boundary latitude. Actual {} is smaller than expected {}".format(actual, expected)
        assert expected <= actual, error_message
        
    def test_latitude_boundary_max(self):
        expected = self.expected_boundaries[3]
        actual = htourism["latitude"].max()
        error_message = "At least one point is bigger than the maximum boundary latitude. Actual {} is bigger than expected {}".format(actual, expected)
        assert  expected >= actual, error_message
    
    def test_longitude_boundary_min(self):
        expected = self.expected_boundaries[0]
        actual = htourism["longitude"].min()
        error_message = "At least one point is smaller than the minimum boundary longitude. Actual {} is smaller than expected {}".format(actual, expected)
        assert expected <= actual, error_message
    
    def test_longitude_boundary_max(self):
        expected = self.expected_boundaries[2]
        actual = htourism["longitude"].max()
        error_message = "At least one point is bigger than the maximum boundary longitude. Actual {} is bigger than expected {}".format(actual, expected)
        assert  expected >= actual, error_message
        
    def test_points_in_polygon(self):
        expected = 0
        not_in_any_polygon = []
        for row in htourism.iterrows():
            row_name = row[1]["institutio"]
            row_geometry = row[1]["geometry"]
            in_any = False
            for polygon in self.expected_polygons:
                if row_geometry.within(polygon):
                    in_any = True
            if in_any == False:
                not_in_any_polygon.append((row_name, row_geometry))
        actual = len(not_in_any_polygon)
        error_message = "{} points were found to be outside polygons representing districts.".format(actual)
        assert expected == actual, error_message
        
        
class TestDataTypes(object):
    def test_data_type_agreement_within_columns(self):
        for column_name in htourism.columns:
            expected_dtype = type(htourism[column_name][0])
            value_index = 0
            while value_index < len(htourism[column_name]):
                value_type = type(htourism[column_name][value_index])
                error_message = "Values in column \"{}\" are not all of same type. Value at index {} is type {}, expected type {}".format(column_name, value_index, value_type, expected_dtype)
                assert value_type == expected_dtype, error_message
                value_index += 1
                
class TestValueAgreement(object):
    def test_district_name_agreement(self):
        dataset_subset = htourism.loc[:,["district_e", "district_t"]]
        for row in dataset_subset.values:
            district_eng = row[0]
            district_tr = row[1]
            actual_similarity = textdistance.jaro_winkler.normalized_similarity(district_tr, district_eng)
            similarity_threshold = 0.50
            error_message = "District name similarity is below similarity treshold. Threshold is {}, similarity is {}".format(similarity_threshold, actual_similarity)
            assert actual_similarity >= similarity_threshold, error_message
            
         
        


