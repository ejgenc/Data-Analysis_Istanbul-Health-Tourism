# -*- coding: utf-8 -*-
"""
------ What is this file? ------

This script targets one file:
    - istanbul_airbnb_processed.csv
    
The script produces kernel-density plots (KDplot) for the distribution of Airbnb
prices in the city of Istanbul. Kdplots are produced for the following
categories:
    - Price data without any tampering
        - Non-grouped price data
        - Price data grouped by district
    - Price data transformed by log10
        - non-grouped price data
    - Price data normalized using IQR.
    - Price data for a specific subset

Returns the plots mentioned above.
"""
#%% --- Import Required Packages ---

import os
from pathlib import Path # To wrap around filepaths
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import iqr, skew, kurtosis, pearsonr

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Import Data ---

import_fp = Path("../../data/processed/istanbul_airbnb_processed.csv")
airbnb_df = pd.read_csv(import_fp, encoding = "utf-8-sig")

#%% --- Visualization One: KDplot for raw price data ---

with plt.style.context('matplotlib_stylesheet_ejg_fixes'):
    
    # --- Create figure and axes ---
    fig_1 = plt.figure(figsize = (10.80,10.80))
    
    ax = fig_1.add_subplot(1,1,1)

    sns.distplot(airbnb_df.loc[:,"price"],
            ax = ax,
            kde = True)
    
#%% --- Visualization Two: KDplot for log10 transformed price data ---

with plt.style.context('matplotlib_stylesheet_ejg_fixes'):
    
    # --- Create figure and axes ---
    fig_2 = plt.figure(figsize = (10.80,10.80))
    
    ax = fig_2.add_subplot(1,1,1)

    sns.distplot(np.log10(airbnb_df.loc[:,"price"]),
            ax = ax,
            kde = True)
    
#%% --- Visualization Three: KDplot for raw and log10 transformed price data ---
# =============================================================================
# 
# with plt.style.context('matplotlib_stylesheet_ejg_fixes'):
#     
#     # --- Create figure and axes ---
#     fig_3 = plt.figure(figsize = (10.80,10.80))
#     
#     ax = fig_2.add_subplot(1,1,1)
# 
#     sns.distplot(np.log10(airbnb_df.loc[:,"price"]),
#             ax = ax,
#             kde = True)
#     
# =============================================================================

