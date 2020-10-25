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

#%% --- Subset Data ---

#Raw price data
prices_raw = airbnb_df.loc[:,"price"]

#Price data transformed with log10 (To see the nuances better)
prices_log10 = np.log10(airbnb_df.loc[:,"price"])

#Price data within +/- 1.5 IQR
price_iqr = iqr(airbnb_df.loc[:,"price"], axis = 0)
    #Calculate q3 and q1
q1 = airbnb_df["price"].quantile(0.25)
q3 = airbnb_df["price"].quantile(0.75)
    #Create min and max mask for +/* 1.5 IQR
min_mask = airbnb_df.loc[:,"price"] >= q1 - (1.5 * price_iqr)
max_mask = airbnb_df.loc[:,"price"] <= q3 + (1.5 * price_iqr)
    #Combine masks
combined_mask = min_mask & max_mask
    #Create subset
prices_within_iqr_1point5 = airbnb_df.loc[combined_mask]


prices = [prices_raw, prices_log10, prices_within_iqr_1point5]
#%% --- Calculate Extra Statistics ---

extrastats_dict = {}

for subset in prices:
    extrastats = None
    
    
#%% --- Visualization One: KDplot for raw and log10 transformed price data ---

with plt.style.context('matplotlib_stylesheet_ejg_fixes'):
    
    # --- Create figure and axes ---
    fig_1 = plt.figure(figsize = (10.80,10.80))
    
    i = 0
    for price_data in prices[:-1]:
        i += 1
        
        ax = fig_1.add_subplot(2,1,i)
        
        sns.distplot(price_data,
                ax = ax,
                color = "#02b72e",
                hist_kws = {
                    "edgecolor" : "black"},
                kde = True,
                kde_kws = {
                    "color" : "black"})    
#%% --- Visualization Two: KDplot for normalized (+/- 1.5 IQR) price data ---
