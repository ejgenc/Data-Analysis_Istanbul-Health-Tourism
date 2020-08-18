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
import pandas as pd

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Define helper functions ---

def sample_and_read_from_df(dataframe, sample_size):
    """

    Sample n(sample_size) rows from the dataset(dataframe). Print out the samples in the console in a column-by-column basis.

    Keyword arguments:
    dataframe -- Accepts a pandas dataframe.
    sample-size -- Accepts an integer. (Default 10.)

    """
    valerror_text = "dataframe must be type pd.DataFrame, got {}".format(type(dataframe))
    assert isinstance(dataframe, pd.DataFrame), ValueError(valerror_text)
    
    valerror_text = "sample_size must be type int, got {}".format(type(sample_size))
    assert isinstance(sample_size, int), ValueError(valerror_text)
    
    index_error_text = ("dataframe length must be larger than or equal to sample_size. "
                        "dataframe length is {}, sample_size is {}").format(len(dataframe), sample_size)
    assert len(dataframe) >= sample_size, IndexError(index_error_text)
    
    dataframe_columns = dataframe.columns
    for column in dataframe_columns:
        print("Commencing with " + column + " column of the dataframe")
        print("")
        for i in range(0,len(dataframe)):
            selection = dataframe.iloc[i]
            print(str(selection[column]).encode("utf-8"))
            print("")
    
def report_null_values(dataframe, report_percentages = True, print_results = False):
    """
    
    Explanation
    ----------
    Calculates the null values in the given dataframe in a column-by-column
    basis. Returns a dataframe whose index is column names of dataframe and whose
    values are the null value numbers.
    
    If report_percentages is True, also calculates of much of each column
    is made out of null values.
    
    If print_results is True, does not return a dataframe but prints
    the information into the console.

    Parameters
    ----------
    dataframe : A pandas dataframe
    report_percentages : Boolean values. True by default.
    print_results : Boolean values. False by default.

    Returns
    -------
    if print_results == False:
        
        null_values_report: A pandas dataframe whose index is column names of
        the original dataframe and whose values are the null value numbers.
        
        if report_percentages == True:
            
            null_values_report: A pandas dataframe whose index is column names of
            the original dataframe and whose values are the null value numbers and percentages.
    
     if print_results == True:
         None
            
    """
    valerror_text = "dataframe must be type pd.DataFrame, got {}".format(type(dataframe))
    assert isinstance(dataframe, pd.DataFrame), ValueError(valerror_text)
    
    #Calculates the sum of null values in a dataframe. x.isnull is a bool mask
    # Boolean "True" is 1. Therefore, it can be summed up using x.sum()
    null_counts = dataframe.isnull().sum()
    
    if report_percentages == True:
        #Divide null count by total length of each col to find a percentage
        null_counts_pct = (null_counts / test_df.shape[0]) * 100
        null_values_report = pd.concat([null_counts, null_counts_pct],
                     axis = 1)
        null_values_report.rename(columns = {0:"null_count",1:"null_percentage"},
                inplace = True)
    else:
        null_values_report = null_counts.rename("null_count")
        
    
    if print_results == True:
        if report_percentages == True:
            for column in null_values_report.index:
                column_null_count = str(null_values_report.loc[column,"null_count"])
                print("Column {} has {} null values.".format(column,column_null_count))
                column_null_percentage = str(null_values_report.loc[column, "null_percentage"])
                print("{} percent of column {} is null values.".format(column_null_percentage,column))
        else:
            for column in null_values_report.index:
                column_null_count = str(null_values_report[column])
                print("Column {} has {} null values.".format(column,column_null_count))
                
    
    else:
        return(null_values_report)
    
    

def visualize_null_values(dataframe, *columns):
    pass

#%% --- AD HOC TESTING ---REMOVE LATER ON ---

#%% -- Set up a test df --
from numpy import arange
array_1 = [5,10,15,6]
array_2 = [2,4,6]
array_3 = [3,6,9]

arrays = [array_1, array_2, array_3]
column_names = ["column " + str(i) for i in arange(0,4)]   

test_df = pd.DataFrame(arrays, columns = column_names)

#%% --- Test funcs on test dataframe ---


#sample_and_read_from_df(test_df, 2)
#sample_and_read_from_df(test_df, 15)
#sample_and_read_from_df(test_df, "2")
#sample_and_read_from_df("a", 15)

#report_null_values("a")
a = report_null_values(test_df)
report_null_values(test_df, print_results= True)
c = report_null_values(test_df, report_percentages = False)
d = report_null_values(test_df, report_percentages = False, print_results= True)

