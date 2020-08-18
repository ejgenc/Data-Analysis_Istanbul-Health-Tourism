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
from src.data_preparation import data_preparation_helper_functions

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Create mock dataframes ---

#Create a random seed
np.random.seed([3,1415])
#Create a dataframe from random np numbers

test_df = pd.DataFrame(np.random.randint(10, size=(50, 5)), columns=list('ABCDE'))
for col in test_df.columns:
    test_df.loc[test_df.sample(frac=0.1).index, col] = np.nan
