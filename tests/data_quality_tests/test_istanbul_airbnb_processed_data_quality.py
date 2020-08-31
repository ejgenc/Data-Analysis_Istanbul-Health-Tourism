# -*- coding: utf-8 -*-
"""
------ What is this file? ------

This test module contains some data quality tests for the istanbul_airbnb_process.csv file
The file can be found at:
    data/processed/istanbul_airbnb_processed.csv

"""
#%% --- Import Required Packages ---

import os
from pathlib import Path # To wrap around filepaths
import pytest
import numpy as np
import pandas as pd
#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Import data ---

import_fp = Path("../../data/processed/istanbul_airbnb_processed.csv")
airbnb = pd.read_csv(import_fp, encoding = "utf-8-sig")

#%% --- Data quality tests ---
 
class TestNullValues(object):
    def test_total_null_values(self):
        expected = 0
        actual = airbnb.isnull().sum().sum()
        error_message = "Dataset contains null values. Expected {} null values, got {}".format(expected,actual)
        assert expected == actual, error_message
        
class TestUniqueness(object):
    def test_total_unique_values_for_column_listing_id(self):
        expected = airbnb.shape[0]
        actual = len(airbnb.loc[:,"listing_id"].unique())
        error_message = "Column listing_id contains non-unique values. Expected {} unique values, got {}".format(expected, actual)
        assert expected == actual, error_message
        
class TestOutliers(object):
    def test_price_outliers_min(self):
        actual = airbnb.loc[:,"price"].min()
        error_message = "Minimum price must be > 0. Got {}".format(actual)
        assert actual > 0, error_message
    
    def test_latitude_boundary(self):
        pass
    
    def test_longitude_boundary(self):
        pass

def TestDataTypes(object):
    def test_data_type_agreement_within_columns(self):
        pass
    
    def test_data_type_agreement_within_object_datatypes(self):
        pass
    
def TestValueAgreement(object):
    def test_district_name_agreement(self):
        pass
         
         
