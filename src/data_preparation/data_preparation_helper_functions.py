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
    
    valerror_text = "sample_size must be type int, got {}".format(type(dataframe))
    assert isinstance(sample_size, int), ValueError(valerror_text)
    
    index_error_text = ("dataframe length must be larger than or equal to sample_size."
                        "dataframe length is {}, sample_size is {}").format(len(df), sample_size)
    assert len(dataframe) >= sample_size, IndexError(index_error_text)
    
    dataframe_columns = dataframe.columns
    for column in dataframe_columns:
        print("Commencing with " + column + " column of the dataframe")
        print("")
        for i in range(0,len(dataframe)):
            selection = dataframe.iloc[i]
            print(str(selection[column]).encode("utf-8-sig"))
            print("")
    
def report_null_values(dataframe, *columns):
    pass

def visualize_null_values(dataframe, *columns):
    pass
    

