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
        
#%%
htourism["institutio"].value_counts
        


