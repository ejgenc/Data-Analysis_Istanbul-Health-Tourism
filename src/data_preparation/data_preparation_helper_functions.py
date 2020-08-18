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
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- FUNCTION: sample_and_read_from_df ---

    # --- Main Function --- #
    
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
            
#%% --- FUNCTION: report_missing_values ---

    # --- Helper Functions ---
    
def is_null_values_dataframe(dataframe):
    """
    Checks if a dataframe is null_values_dataframe.

    Parameters
    ----------
    dataframe : pandas.DataFrame

    Returns
    -------
    Returns Boolean True if the dataframe is a null_values_dataframe.
    Returns Boolean False if the dataframe is not a null_values_dataframe

    """
    valerror_text = "dataframe must be type pd.DataFrame, got {}".format(type(dataframe))
    assert isinstance(dataframe, pd.DataFrame), ValueError(valerror_text)
    
    is_null_values_dataframe = False
    
    if "null_count" in dataframe.columns:
        is_null_values_dataframe = True
        
    return is_null_values_dataframe

def is_extended_null_values_dataframe(null_values_dataframe):
    """
    Checks if dataframe is a extended null_values_dataframe

    Parameters
    ----------
    null_values_dataframe : pandas.DataFrame

    Returns
    -------
    Returns Boolean True if the dataframe is a extended null_values_dataframe.
    Returns Boolean False if the dataframe is not a extended null_values_dataframe

    """
    valerror_text = "dataframe must be type pd.DataFrame, got {}".format(type(null_values_dataframe))
    assert isinstance(null_values_dataframe, pd.DataFrame), ValueError(valerror_text)
    
    valerror_text = "dataframe does not contain null_count information."
    assert is_null_values_dataframe(null_values_dataframe), ValueError(valerror_text)
    
    is_extended_null_values_dataframe = False
    
    if "null_percentage" in null_values_dataframe.columns:
        is_extended_null_values_dataframe = True
        
    return is_extended_null_values_dataframe

def plot_null_values_bar_chart(null_values_dataframe):
    """
    Creates a bar chart from a null_values_dataframe.
    If the null_values_dataframe is an extended null_values_dataframe,
    creates a double bar chart view which displays percentage information.
    
    Parameters
    ----------
    null_values_dataframe : pandas.DataFrame.

    Returns
    -------
    Returns a matplotlib.pyplot.Figure object.

    """
    
    valerror_text = "dataframe must be type pd.DataFrame, got {}".format(type(null_values_dataframe))
    assert isinstance(null_values_dataframe, pd.DataFrame), ValueError(valerror_text)
    
    valerror_text = "dataframe does not contain null_count information."
    assert is_null_values_dataframe(null_values_dataframe), ValueError(valerror_text)
    
    fig = plt.Figure(figsize = (9.60,7.20))
    
    # Ax creating is wrapped inside if-else statement because creating
    #two instances of ax_1 DOES NOT override each other.
    if is_extended_null_values_dataframe(null_values_dataframe):
        ax_1 = fig.add_subplot(1,2,1)
        ax_2 = fig.add_subplot(1,2,2)
        
    else:
        ax_1 = fig.add_subplot(1,1,1)

    
    labels = list(null_values_dataframe.index)
    
    from numpy import arange
    bar_positions = arange(len(labels)) + 1
    
    bar_heights_1 = null_values_dataframe.loc[:,"null_count"]
    
    if is_extended_null_values_dataframe(null_values_dataframe):
        bar_heights_2 = null_values_dataframe.loc[:,"null_percentage"]
        
    ax_1.bar(bar_positions, bar_heights_1,
             width = 0.7,
             align = "center")
    
    ax_1.set_xticks(bar_positions)
    ax_1.set_xticklabels(labels, rotation = 90)
    
    if is_extended_null_values_dataframe(null_values_dataframe):
        ax_2.bar(bar_positions, bar_heights_2,
                 width = 0.7,
                 align = "center")
        
        ax_2.set_xticks(bar_positions)
        ax_2.set_xticklabels(labels, rotation = 90)
    
    plt.show()
    return fig

def plot_null_values_matrix(dataframe):
    """
    

    Parameters
    ----------
    dataframe : TYPE
        DESCRIPTION.

    Returns
    -------
    fig : TYPE
        DESCRIPTION.

    """
    
    valerror_text = "dataframe must be type pd.DataFrame, got {}".format(type(dataframe))
    assert isinstance(dataframe, pd.DataFrame), ValueError(valerror_text)
    
    
    fig = plt.Figure(figsize = (9.60,7.20))
    ax = fig.add_subplot()
    #Create a boolean dataframe based on whether values are null or not
    df_null = dataframe.isnull()
    #create a heatmap of the boolean dataframe
    sns.heatmap(df_null,
                cbar = False)
    plt.xticks(rotation=90, size='x-large')
    plt.show()
    return fig   

    # --- Subfunction : calculate_null_values ---
        
def calculate_null_values(dataframe, calculate_percentages = True):
    """
    
    Calculates the null values in the given dataframe in a column-by-column
    basis. Returns a dataframe whose index is column names of dataframe and whose
    values are the null value numbers.
    
    If report_percentages is True, also calculates of much of each column
    is made out of null values.

    Parameters
    ----------
    dataframe : pandas.DataFrame.
    calculate_percentages : Boolean value, optional
        Sets whether the null value percentage of columns will be calculated.
        The default is True.

    Returns
    -------
    null_values_report : pandas.DataFrame.
        A pandas.DataFrame that encodes information about
        null values in the original dataframe in a column-by-column basis.
        
    """
    valerror_text = "dataframe must be type pd.DataFrame, got {}".format(type(dataframe))
    assert isinstance(dataframe, pd.DataFrame), ValueError(valerror_text)
    
    null_counts = dataframe.isnull().sum()
    
    if calculate_percentages == True:
        #Divide null count by total length of each col to find a percentage
        null_counts_pct = (null_counts / test_df.shape[0]) * 100
        null_values_report = pd.concat([null_counts, null_counts_pct],
                 axis = 1)
        null_values_report.rename(columns = {0:"null_count",1:"null_percentage"},
            inplace = True)
    else:
        null_values_report = null_counts.rename("null_count").to_frame()
        
    return null_values_report

    # --- Subfunction : print_null_values ---
    
def print_null_values(null_values_dataframe):
    """
    
    Prints out into the console a formatted message that explains
    a null_values_dataframe.
    
    Parameters
    ----------
    null_values_dataframe : pandas.DataFrame.
        A pandas.DataFrame that is produced as the result of calling
        calculate_null_values() on a dataframe. Has to contain a column
        called "null_count" at minimum.
 

    Returns
    -------
    None.

    """
    
    valerror_text = "dataframe must be type pd.DataFrame, got {}".format(type(null_values_dataframe))
    assert isinstance(null_values_dataframe, pd.DataFrame), ValueError(valerror_text)
    
    valerror_text = "dataframe does not contain null_count information."
    assert is_null_values_dataframe(null_values_dataframe), ValueError(valerror_text)
    
    if is_extended_null_values_dataframe(null_values_dataframe):
        for column in null_values_dataframe.index:
            column_null_count = str(null_values_dataframe.loc[column,"null_count"])
            print("Column {} has {} null values.".format(column,column_null_count))
            column_null_percentage = str(null_values_dataframe.loc[column, "null_percentage"])
            print("{} percent of column {} is null values.".format(column_null_percentage,column))
    else:
        for column in null_values_dataframe.index:
            column_null_count = str(null_values_dataframe.loc[column,"null_count"])
            print("Column {} has {} null values.".format(column,column_null_count))
            

    # --- Subfunction : visualize_null_values ---
            
def visualize_null_values(null_values_dataframe, kind = "bar_chart"):
    """

    Lorem ipsum dolor sit amet

    Parameters
    ----------
    null_values_dataframe : TYPE
        DESCRIPTION.
    kind : TYPE, optional
        DESCRIPTION. The default is "bar_chart".

    Returns
    -------
    None.

    """
    valerror_text = "dataframe must be type pd.DataFrame, got {}".format(type(null_values_dataframe))
    assert isinstance(null_values_dataframe, pd.DataFrame), ValueError(valerror_text)
    
    valerror_text = "dataframe does not contain null_count information."
    assert is_null_values_dataframe(null_values_dataframe), ValueError(valerror_text)
    
    accepted_kinds = ["bar_chart", "matrix", "heatmap"]
    valerror_text = "Parameter kind must be a string and one of bar_chart, matrix or heatmap. Got {} as type {}.".format(str(kind), type(kind))
    assert str(kind) in accepted_kinds, ValueError(valerror_text)
    
    if kind == "bar_chart":
        plot = plot_null_values_bar_chart(null_values_dataframe)
    
    elif kind == "matrix":
        raise NotImplementedError
    
    elif kind == "heatmap":      
        raise NotImplementedError
    
    return plot

    # --- Main function: report_null_values ---

def report_null_values(dataframe, calculate_percentages = True,
                       visualize_results = False, print_results = False):
    
    if calculate_percentages == True:
        null_values_dataframe = calculate_null_values(dataframe, calculate_percentages = True)
    else:
        null_values_dataframe = calculate_null_values(dataframe, calculate_percentages = False)
        
    if visualize_results == True:
        plot = visualize_null_values(null_values_dataframe)
        return plot
    
    elif print_results == True:
        print_null_values(null_values_dataframe)
    
    else:
        return null_values_dataframe