# -*- coding: utf-8 -*-
"""
------ What is this file? ------

This script contains some helper functions that are used in the scripts found found under src/data_preparation.
The unit tests for these functions can be found at:
     tests/unit_tests/data_preparation/test_data_preparation_helper_functions.py

"""
#%% --- Import Required Packages ---

import os
from pathlib import Path # To wrap around filepaths
import pytest
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.data_preparation import data_preparation_helper_functions as functions
from numpy import arange

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Create mock test objects ---

    #%% --- Normal dataframe ---

#Create a random seed
np.random.seed([3,1415])
#Create a dataframe from random np numbers
test_df = pd.DataFrame(np.random.randint(10, size=(100, 5)),
                       columns=list('ABCDE'))
#Select ten percent of each column and turn it into np.nan
for col in test_df.columns:
    test_df.loc[test_df.sample(frac=0.1).index, col] = np.nan
    
    #%% --- null_values dataframe ---

#Create 5 indexes
index_names = ["column " + str(i) for i in arange(1,6) ]

column_names = ["null_count"]

test_null_values_df = pd.DataFrame(np.random.randint(10, size = (5,1)),
                                   columns = column_names,
                                   index = index_names)
    
#Create 2 columns for extended
column_names_extended = ["null_count","null_percentage"]

#Create a 5 x 2 dataframe from random np numbers for extended null values df
test_null_values_df_extended = pd.DataFrame(np.random.randint(10, size = (5,2)),
                                   columns = column_names_extended,
                                   index = index_names)
    
    #%% --- other  ---

test_str = "Test"
test_int = 10
test_float = 10.5
test_bool = False
test_sample_size_int_correct = 5
test_sample_size_int_wrong = 105
    
#%% --- Testing ---
#%%     --- Test: sample_and_read_from_df

class TestSampleAndReadFromDf(object):
    def test_valerror_on_nondf_dataframe_str(self):
        test_dataframe = test_str
        test_sample_size = test_sample_size_int_correct
        expected_message = "dataframe must be type pd.DataFrame, got {}".format(type(test_dataframe))
        with pytest.raises(ValueError) as exception_info:
            functions.sample_and_read_from_df(test_dataframe, test_sample_size)
            error_message = "Expected following message: {}. Got the following {}"
        assert exception_info.match(expected_message), error_message
        
    def test_valerror_on_nondf_dataframe_float(self):
        test_dataframe = test_float
        test_sample_size = test_sample_size_int_correct
        expected_message = "dataframe must be type pd.DataFrame, got {}".format(type(test_dataframe))
        with pytest.raises(ValueError) as exception_info:
            functions.sample_and_read_from_df(test_dataframe, test_sample_size)
            error_message = "Expected following message: {}. Got the following {}"
        assert exception_info.match(expected_message), error_message
        
    def test_valerror_on_nonint_sample_size_str(self):
        test_dataframe = test_df
        test_sample_size = test_str
        expected_message = "sample_size must be type int, got {}".format(type(test_sample_size))
        with pytest.raises(ValueError) as exception_info:
            functions.sample_and_read_from_df(test_dataframe, test_sample_size)
            error_message = "Expected the following message: {}. Got the following: {}"
        assert exception_info.match(expected_message), error_message
        
    def test_valerror_on_nonint_sample_size_float(self):
        test_dataframe = test_df
        test_sample_size = test_float
        expected_message = "sample_size must be type int, got {}".format(type(test_sample_size))
        with pytest.raises(ValueError) as exception_info:
            functions.sample_and_read_from_df(test_dataframe, test_sample_size)
            error_message = "Expected the following message: {}. Got the following: {}"
        assert exception_info.match(expected_message), error_message
        
    def test_indexerror_on_wrong_sample_size(self):
        test_dataframe = test_df
        test_sample_size = test_sample_size_int_wrong
        expected_message = ("dataframe length must be larger than or equal to sample_size. "
                        "dataframe length is {}, sample_size is {}").format(len(test_dataframe), test_sample_size)
        with pytest.raises(IndexError) as exception_info:
            functions.sample_and_read_from_df(test_dataframe, test_sample_size)
            error_message = "Expected the following message: {}. Got the following: {}"
        assert exception_info.match(expected_message), error_message
        
#%%     --- Test: report_null_values ---
#%%         --- Test helper function: is_null_values_dataframe ---

class TestIsNullValuesDataframe(object):
    def test_valerror_on_nondf_dataframe_str(self):
        test_dataframe = test_str
        expected_message = "dataframe must be type pd.DataFrame, got {}".format(type(test_dataframe))
        with pytest.raises(ValueError) as exception_info:
            functions.is_null_values_dataframe(test_dataframe)
            error_message = "Expected the following message: {}. Got the following: {}"
        assert exception_info.match(expected_message), error_message
        
    def test_valerror_on_nondf_dataframe_bool(self):
        test_dataframe = test_bool
        expected_message = "dataframe must be type pd.DataFrame, got {}".format(type(test_dataframe))
        with pytest.raises(ValueError) as exception_info:
            functions.is_null_values_dataframe(test_dataframe)
            error_message = "Expected the following message: {}. Got the following: {}"
        assert exception_info.match(expected_message), error_message
        
    def test_on_non_null_values_dataframe(self):
        test_dataframe = test_df
        expected = False
        actual = functions.is_null_values_dataframe(test_dataframe)
        error_message = "Expected {} as output, got {}".format(expected,actual)
        assert expected is actual, error_message
    
    def test_on_null_values_dataframe(self):
        test_dataframe = test_null_values_df
        expected = True
        actual = functions.is_null_values_dataframe(test_dataframe)
        error_message = "Expected {} as output, got {}".format(expected,actual)
        assert expected is actual, error_message
        
#%%         --- Test helper function: is_extended_null_values_dataframe ---        
        
class TestIsExtendedNullValuesDataframe(object):
    def test_valerror_on_nondf_dataframe_str(self):
        test_dataframe = test_str
        expected_message = "dataframe must be type pd.DataFrame, got {}".format(type(test_dataframe))
        with pytest.raises(ValueError) as exception_info:
            functions.is_extended_null_values_dataframe(test_dataframe)
            error_message = "Expected the following message: {}. Got the following: {}"
        assert exception_info.match(expected_message), error_message
    
    def test_valerror_on_nondf_dataframe_float(self):
        test_dataframe = test_float
        expected_message = "dataframe must be type pd.DataFrame, got {}".format(type(test_dataframe))
        with pytest.raises(ValueError) as exception_info:
            functions.is_extended_null_values_dataframe(test_dataframe)
            error_message = "Expected the following message: {}. Got the following: {}"
        assert exception_info.match(expected_message), error_message
    
    def test_valerror_on_non_null_values_dataframe(self):
        test_dataframe = test_df
        expected_message = "dataframe does not contain null_count information."
        with pytest.raises(ValueError) as exception_info:
            functions.is_extended_null_values_dataframe(test_df)
            error_message = "Expected the following message: {}. Got the following: {}"
        assert exception_info.match(expected_message), error_message
    
    def test_on_null_values_dataframe(self):
        test_dataframe = test_null_values_df
        expected = False
        actual = functions.is_extended_null_values_dataframe(test_dataframe)
        error_message = "Expected {} as output, got {}".format(expected,actual)
        assert expected is actual, error_message
        
    
    def test_on_extended_null_values_dataframe(self):
        test_dataframe = test_null_values_df_extended
        expected = True
        actual = functions.is_extended_null_values_dataframe(test_dataframe)
        error_message = "Expected {} as output, got {}".format(expected,actual)
        assert expected is actual, error_message
        
#%%         --- Test helper function: plot_null_values_bar_chart---

class TestPlotNullValuesBarChart(object):
    def test_valerror_on_nondf_dataframe_str(self):
            test_dataframe = test_str
            expected_message = "dataframe must be type pd.DataFrame, got {}".format(type(test_dataframe))
            with pytest.raises(ValueError) as exception_info:
                functions.plot_null_values_bar_chart(test_dataframe)
                error_message = "Expected the following message: {}. Got the following: {}"
            assert exception_info.match(expected_message), error_message
        
    def test_valerror_on_nondf_dataframe_bool(self):
            test_dataframe = test_bool
            expected_message = "dataframe must be type pd.DataFrame, got {}".format(type(test_dataframe))
            with pytest.raises(ValueError) as exception_info:
                functions.plot_null_values_bar_chart(test_dataframe)
                error_message = "Expected the following message: {}. Got the following: {}"
            assert exception_info.match(expected_message), error_message
        
    def test_valerror_on_non_null_values_dataframe(self):
            test_dataframe = test_df
            expected_message = "dataframe does not contain null_count information."
            with pytest.raises(ValueError) as exception_info:
                functions.plot_null_values_bar_chart(test_df)
                error_message = "Expected the following message: {}. Got the following: {}"
            assert exception_info.match(expected_message), error_message
            
    def test_axisnumber_on_null_values_dataframe:
        pass
    
    def test_axisnumber_on_extended_null_values_dataframe:
        pass
        
        
        
        
        

        
