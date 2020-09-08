# -*- coding: utf-8 -*-
"""
------ What is this file? ------

This test module contains some tests for the data_preparation_helper_functions.py script.
The script can be found at:
    src/helper_functions/data_preparation_helper_functions.py

"""
#%% --- Import Required Packages ---

import os
from pathlib import Path # To wrap around filepaths
import pytest
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.helper_functions import data_preparation_helper_functions as functions
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
        error_message = "Expected following message: {}. Got the following {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
        
    def test_valerror_on_nondf_dataframe_float(self):
        test_dataframe = test_float
        test_sample_size = test_sample_size_int_correct
        expected_message = "dataframe must be type pd.DataFrame, got {}".format(type(test_dataframe))
        with pytest.raises(ValueError) as exception_info:
            functions.sample_and_read_from_df(test_dataframe, test_sample_size)
        error_message = "Expected following message: {}. Got the following {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
        
    def test_valerror_on_nonint_sample_size_str(self):
        test_dataframe = test_df
        test_sample_size = test_str
        expected_message = "sample_size must be type int, got {}".format(type(test_sample_size))
        with pytest.raises(ValueError) as exception_info:
            functions.sample_and_read_from_df(test_dataframe, test_sample_size)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
        
    def test_valerror_on_nonint_sample_size_float(self):
        test_dataframe = test_df
        test_sample_size = test_float
        expected_message = "sample_size must be type int, got {}".format(type(test_sample_size))
        with pytest.raises(ValueError) as exception_info:
            functions.sample_and_read_from_df(test_dataframe, test_sample_size)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
        
    def test_indexerror_on_wrong_sample_size(self):
        test_dataframe = test_df
        test_sample_size = test_sample_size_int_wrong
        expected_message = ("dataframe length must be larger than or equal to sample_size. "
                        "dataframe length is {}, sample_size is {}").format(len(test_dataframe), test_sample_size)
        with pytest.raises(IndexError) as exception_info:
            functions.sample_and_read_from_df(test_dataframe, test_sample_size)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
        
#%%     --- Test: report_null_values ---
#%%         --- Test helper function: is_null_values_dataframe ---

class TestIsNullValuesDataframe(object):
    def test_valerror_on_nondf_dataframe_str(self):
        test_dataframe = test_str
        expected_message = "dataframe must be type pd.DataFrame, got {}".format(type(test_dataframe))
        with pytest.raises(ValueError) as exception_info:
            functions.is_null_values_dataframe(test_dataframe)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
        
    def test_valerror_on_nondf_dataframe_bool(self):
        test_dataframe = test_bool
        expected_message = "dataframe must be type pd.DataFrame, got {}".format(type(test_dataframe))
        with pytest.raises(ValueError) as exception_info:
            functions.is_null_values_dataframe(test_dataframe)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
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
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_valerror_on_nondf_dataframe_float(self):
        test_dataframe = test_float
        expected_message = "dataframe must be type pd.DataFrame, got {}".format(type(test_dataframe))
        with pytest.raises(ValueError) as exception_info:
            functions.is_extended_null_values_dataframe(test_dataframe)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_valerror_on_non_null_values_dataframe(self):
        test_dataframe = test_df
        expected_message = "dataframe does not contain null_count information."
        with pytest.raises(ValueError) as exception_info:
            functions.is_extended_null_values_dataframe(test_dataframe)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
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
            error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
            assert exception_info.match(expected_message), error_message
        
    def test_valerror_on_nondf_dataframe_bool(self):
            test_dataframe = test_bool
            expected_message = "dataframe must be type pd.DataFrame, got {}".format(type(test_dataframe))
            with pytest.raises(ValueError) as exception_info:
                functions.plot_null_values_bar_chart(test_dataframe)
            error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
            assert exception_info.match(expected_message), error_message
        
    def test_valerror_on_non_null_values_dataframe(self):
            test_dataframe = test_df
            expected_message = "dataframe does not contain null_count information."
            with pytest.raises(ValueError) as exception_info:
                functions.plot_null_values_bar_chart(test_dataframe)
            error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
            assert exception_info.match(expected_message), error_message
            
    def test_axisnumber_on_null_values_dataframe(self):
        test_dataframe = test_null_values_df
        expected = 1
        actual = len(functions.plot_null_values_bar_chart(test_dataframe).axes)
        error_message = "Expected {} as total axis number, got {}".format(expected,actual)
        assert expected is actual, error_message
    
    def test_axisnumber_on_extended_null_values_dataframe(self):
        test_dataframe = test_null_values_df_extended
        expected = 2
        actual = len(functions.plot_null_values_bar_chart(test_dataframe).axes)
        error_message = "Expected {} as total axis number, got {}".format(expected,actual)
        assert expected is actual, error_message
        
    def test_xticklabel_number_on_null_values_dataframe(self):
        test_dataframe = test_null_values_df
        expected = 5
        actual = len(functions.plot_null_values_bar_chart(test_dataframe).axes[0].get_xticklabels())
        error_message = "Expected {} total x-axis ticklabels, got {}".format(expected,actual)
        assert expected is actual, error_message
        
#%%         --- Test helper function: plot_null_values_matrix ---

class TestPlotNullValuesMatrix(object):
    def test_valerror_on_nondf_dataframe_float(self):
        test_dataframe = test_float
        expected_message = "dataframe must be type pd.DataFrame, got {}".format(type(test_dataframe))
        with pytest.raises(ValueError) as exception_info:
            functions.plot_null_values_matrix(test_dataframe)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message        
    
    def test_valerror_on_nondf_dataframe_int(self):
        test_dataframe = test_int
        expected_message = "dataframe must be type pd.DataFrame, got {}".format(type(test_dataframe))
        with pytest.raises(ValueError) as exception_info:
            functions.plot_null_values_matrix(test_dataframe)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
#%%     --- Test subfunction: calculate_null_values ---

class TestCalculateNullValues(object):
    def test_valerror_on_nondf_dataframe_str(self):
        test_dataframe = test_str
        expected_message = "dataframe must be type pd.DataFrame, got {}".format(type(test_dataframe))
        with pytest.raises(ValueError) as exception_info:
            functions.calculate_null_values(test_dataframe)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message        
    
    def test_valerror_on_nondf_dataframe_int(self):
        test_dataframe = test_int
        expected_message = "dataframe must be type pd.DataFrame, got {}".format(type(test_dataframe))
        with pytest.raises(ValueError) as exception_info:
            functions.calculate_null_values(test_dataframe)
        error_message = "Expected the following message: {}. Got the following: {}"
        assert exception_info.match(expected_message), error_message
        
    def test_valerror_on_nonbool_calculate_percentages(self):
        test_dataframe = test_df
        test_calculate_percentages = test_str
        expected_message = "calculate_percentages must be type boolean True or False, got {}".format(type(test_calculate_percentages))
        with pytest.raises(ValueError) as exception_info:
            functions.calculate_null_values(test_dataframe, test_calculate_percentages)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
        
    def test_column_names_for_calculate_percentages_true(self):
        test_dataframe = test_df
        expected = ["null_count", "null_percentage"]
        actual = list(functions.calculate_null_values(test_dataframe).columns)
        error_message = ("Columns are not correctly named. Expected names {}, got {}".format(expected, actual))
        assert sorted(expected) == sorted(actual), error_message
    
    def test_column_names_for_calculate_percentages_false(self):
        test_dataframe = test_df
        expected = ["null_count"]
        actual = list(functions.calculate_null_values(test_dataframe, calculate_percentages = False).columns)
        error_message = ("Columns are not correctly named. Expected names {}, got {}".format(expected, actual))
        assert sorted(expected) == sorted(actual), error_message
        
    def test_null_count_sum_for_calculate_percentages_true(self):
        test_dataframe = test_df
        expected = 50
        actual = int(functions.calculate_null_values(test_dataframe).loc[:,"null_count"].sum())
        error_message = "Sum of null_count column is not correct. Expected {}, got {}".format(expected, actual)
        assert expected == actual, error_message
    
    def test_null_count_sum_for_calculate_percentages_false(self):
        test_dataframe = test_df
        expected = 50
        actual = int(functions.calculate_null_values(test_dataframe, calculate_percentages = False).loc[:,"null_count"].sum())
        error_message = "Sum of null_count column is not correct. Expected {}, got {}".format(expected, actual)
        assert expected == actual, error_message
    
    def test_null_percentage_sum_for_calculate_percentages_true(self):
        test_dataframe = test_df
        expected = float(50)
        actual = float(functions.calculate_null_values(test_dataframe).loc[:,"null_percentage"].sum())
        error_message = "Sum of null_count column is not correct. Expected {}, got {}".format(expected, actual)
        assert expected == actual, error_message
        
    def test_returned_is_dataframe(self):
        test_dataframe = test_df
        expected = pd.DataFrame
        actual = type(functions.calculate_null_values(test_dataframe))
        error_message = "Return object is not correct. Expected {}, got {}".format(expected,actual)
        assert not isinstance(actual, expected), error_message
    
    def test_returned_dataframe_shape(self):
        test_dataframe = test_df
        expected = (5,2)
        actual = functions.calculate_null_values(test_dataframe).shape
        error_message = "Dataframe shape is wrong. Expected {}, got {}".format(expected, actual)
        assert expected == actual, error_message
        
#%%     --- Test subfunction: print_null_values ---

class TestPrintNullValues(object):
    def test_valerror_on_nondf_dataframe_int(self):
        test_dataframe = test_int
        expected_message = "dataframe must be type pd.DataFrame, got {}".format(type(test_dataframe))
        with pytest.raises(ValueError) as exception_info:
            functions.print_null_values(test_dataframe)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_valerror_on_nondf_dataframe_float(self):
        test_dataframe = test_float
        expected_message = "dataframe must be type pd.DataFrame, got {}".format(type(test_dataframe))
        with pytest.raises(ValueError) as exception_info:
            functions.print_null_values(test_dataframe)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
        
    def test_valerror_on_non_null_values_dataframe(self):
        test_dataframe = test_df
        expected_message = "dataframe does not contain null_count information."
        with pytest.raises(ValueError) as exception_info:
            functions.print_null_values(test_dataframe)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message

#%%     --- Test subfunction: visualize_null_values ---

class TestVisualizeNullValues(object):
    def test_valerror_on_nondf_dataframe_bool(self):
        test_dataframe = test_bool
        expected_message = "dataframe must be type pd.DataFrame, got {}".format(type(test_dataframe))
        with pytest.raises(ValueError) as exception_info:
            functions.visualize_null_values(test_dataframe)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_valerror_on_nondf_dataframe_int(self):
        test_dataframe = test_int
        expected_message = "dataframe must be type pd.DataFrame, got {}".format(type(test_dataframe))
        with pytest.raises(ValueError) as exception_info:
            functions.visualize_null_values(test_dataframe)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_valerror_on_non_null_values_dataframe(self):
        test_dataframe = test_df
        expected_message = "dataframe does not contain null_count information."
        with pytest.raises(ValueError) as exception_info:
            functions.visualize_null_values(test_dataframe)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message

    
    def test_valerror_on_invalid_kind_str(self):
        test_dataframe = test_null_values_df
        test_kind = "invalid_kind"
        expected_message = "Parameter kind must be a string and one of bar_chart, matrix or heatmap. Got \"{}\" as type {}.".format(str(test_kind), type(test_kind))
        with pytest.raises(ValueError) as exception_info:
            functions.visualize_null_values(test_dataframe, kind = test_kind)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message

#%% --- Test main function: report_null_values ---

class TestReportNullValues(object):
    def test_valerror_on_nondf_dataframe_bool(self):
        test_dataframe = test_bool
        expected_message = "dataframe must be type pd.DataFrame, got {}".format(type(test_dataframe))
        with pytest.raises(ValueError) as exception_info:
            functions.report_null_values(test_dataframe)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
    
    def test_valerror_on_nondf_dataframe_int(self):
        test_dataframe = test_int
        expected_message = "dataframe must be type pd.DataFrame, got {}".format(type(test_dataframe))
        with pytest.raises(ValueError) as exception_info:
            functions.report_null_values(test_dataframe)
        error_message = "Expected the following message: {}. Got the following: {}".format(expected_message, exception_info)
        assert exception_info.match(expected_message), error_message
                    
    def test_valerror_on_two_parameters_true(self):
        test_dataframe = test_df
        test_parameter_visualize_results = True
        test_parameter_print_results = True
        expected_message = "Parameters visualize_results and print_results cannot be both boolean True."
        with pytest.raises(ValueError) as exception_info:
            functions.report_null_values(test_dataframe,
                                         visualize_results = test_parameter_visualize_results,
                                         print_results = test_parameter_print_results)
        assert exception_info.match(expected_message), error_message
                
    def test_returned_is_dataframe_on_calculate_percentages_true(self):
        test_dataframe = test_df
        expected = pd.DataFrame
        actual = type(functions.report_null_values(test_dataframe, calculate_percentages = True))
        error_message = "Return object is not correct. Expected {}, got {}".format(expected,actual)
        assert not isinstance(actual, expected), error_message
    
    def test_returned_is_dataframe_on_calculate_percentages_false(self):
        test_dataframe = test_df
        expected = pd.DataFrame
        actual = type(functions.report_null_values(test_dataframe, calculate_percentages = False))
        error_message = "Return object is not correct. Expected {}, got {}".format(expected,actual)
        assert not isinstance(actual, expected), error_message
        

    
    

        
        
        

        
