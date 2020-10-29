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
prices_within_iqr_1point5 = airbnb_df.loc[combined_mask,"price"]

prices = [prices_raw, prices_log10, prices_within_iqr_1point5]

#Create a group-by per district
airbnb_grouped_by_district = airbnb_df.groupby(by = "district_eng")
airbnb_districts_prices = airbnb_grouped_by_district["price"]

#Create a group-by per district for normalized prices

prices_normalized_within_iqr_1point5 = airbnb_df.loc[combined_mask,["district_eng","price"]]
airbnb_grouped_by_district_normalized = prices_normalized_within_iqr_1point5.groupby(by = "district_eng")
airbnb_districts_prices_normalized = airbnb_grouped_by_district_normalized["price"]
#%% --- Calculate Extra Statistics ---
# Min max Mean median std skew kurtosis

functions = [min, max,np.mean, np.median, np.std, skew, kurtosis]
extrastats_list = []

for subset in prices:
    extrastats = [function(subset) for function in functions]
    extrastats_list.append(extrastats)
    
#%% --- Visualization One: Histogram for raw and log10 transformed price data ---

with plt.style.context('matplotlib_stylesheet_ejg_fixes'):
    
    # --- Create figure and axes ---
    fig_1 = plt.figure(figsize = (10.80,10.80))
    
    i = 0
    for price_data in prices[:-1]:
        i += 1
        
        ax = fig_1.add_subplot(2,1,i)
        
    # --- Plot the data ---
        sns.distplot(price_data,
                ax = ax,
                color = "#02b72e",
                hist_kws = {
                    "edgecolor" : "black",
                    "alpha" : 0.6},
                kde = False)  
    # --- Text ---
    
    # --- Annotate placeholders ---

    fig_1.axes[0].text(x = 0.70, y = 0.70,
      s = "PLACEHOLDER",
      transform = fig_1.axes[0].transAxes,
      fontfamily = "Arial",
      fontsize = 14,
      fontweight = "bold")
    
    fig_1.axes[0].text(x = 0.01, y = 0.50,
      s = str(extrastats_list[0]),
      transform = fig_1.axes[0].transAxes,
      fontfamily = "Arial",
      fontsize = 10,
      fontweight = "bold")
    
    fig_1.axes[0].text(x = 0.3, y = 0.20,
      s = "Min max mean median std skew kurtosis",
      transform = fig_1.axes[0].transAxes,
      fontfamily = "Arial",
      fontsize = 10,
      fontweight = "bold")
    
    # --- Annotate extra information ----
    
    fig_1.axes[0].text(x = 0.1, y = 0.7,
                s = ("Utilizing a histogram to visualize the distribution\nof the Airbnb "
                "rental prices offers no information\nbecause of the extreme positive skew "
                "of the dataset."),
                transform = fig_1.axes[0].transAxes,
                fontfamily = "Arial",
                fontsize = 14,
                fontweight = "bold",)
    
    fig_1.axes[1].text(x = 0.4, y = 0.7,
                s = ("However, log10 transforming the data allows us\n"
                     "to see the overall distribution better."),
                transform = fig_1.axes[1].transAxes,
                fontfamily = "Arial",
                fontsize = 14,
                fontweight = "bold",)
        
    # --- Set x-axis labels ---
    fig_1.axes[0].set_xlabel("Price",
                             fontfamily = "Arial",
                             fontsize = 16,
                             fontweight = "bold")
    
    fig_1.axes[1].set_xlabel("Price (log10 transformed)",
                             fontfamily = "Arial",
                             fontsize = 16,
                             fontweight = "bold")
    
    # --- Set y-axis label ---
    
    fig_1.text(x = 0.05, y = 0.50,
          s = "Count",
          fontfamily = "Arial",
          fontsize = 16,
          fontweight = "bold",
          rotation = 90)
        
            
    # --- Set figure title ---
    
    fig_1.suptitle("The distribution of Airbnb rental prices.",
                   x = 0.50,
                   y = 0.90,
                   horizontalalignment = "center",
                   fontfamily = "Arial",
                   fontsize = 18,
                   fontweight = "bold",)
         
            
#%% --- Visualization Two: Histogram for normalized (+/- 1.5 IQR) price data ---

with plt.style.context('matplotlib_stylesheet_ejg_fixes'):
    
    # --- Create figure and axes ---
    
    fig_2 = plt.figure(figsize = (10.80,10.80))
       
    ax = fig_2.add_subplot(1,1,1)
    
    # --- Plot the data ---
    
    sns.distplot(prices[2],
            ax = ax,
            color = "#02b72e",
            hist_kws = {
                "edgecolor" : "black",
                "alpha" : 0.6},
            kde = False)  
    
    # --- Text ---

    # --- Annotate placeholders ---

    fig_2.text(x = 0.70, y = 0.70,
      s = "PLACEHOLDER",
      transform = ax.transAxes,
      fontfamily = "Arial",
      fontsize = 14,
      fontweight = "bold")
    
    fig_2.text(x = 0.01, y = 0.50,
      s = str(extrastats_list[2]),
      transform = ax.transAxes,
      fontfamily = "Arial",
      fontsize = 10,
      fontweight = "bold")
    
    fig_2.text(x = 0.3, y = 0.20,
      s = "Min max mean median std skew kurtosis",
      transform = ax.transAxes,
      fontfamily = "Arial",
      fontsize = 10,
      fontweight = "bold")
    
    # --- Set x-axis labels ---
    ax.set_xlabel("Price (normalized)",
                    fontfamily = "Arial",
                    fontsize = 16,
                    fontweight = "bold")
        
    # --- Set y-axis label ---
    ax.set_ylabel("Count",
                fontfamily = "Arial",
                fontsize = 16,
                fontweight = "bold")
    
    # --- Set Fig Title ---
    fig_2.suptitle("The distribution of normalized Airbnb rental prices.",
                   x = 0.50,
                   y = 0.90,
                   horizontalalignment = "center",
                   fontfamily = "Arial",
                   fontsize = 18,
                   fontweight = "bold",)
    
#%% --- Visualization Three: Small multiples histogram for Airbnb price data
# faceted by district

with plt.style.context('matplotlib_stylesheet_ejg_fixes'):

    # --- Create figure and axes ---
    i = 0
   
    fig_3 = plt.figure(figsize = (25.00, 25.00))
   
    for group in airbnb_districts_prices.groups:
        
        price_n_of_observations = len(airbnb_districts_prices.get_group(group))
        price_mean = np.mean(airbnb_districts_prices.get_group(group))
        price_median = np.median(airbnb_districts_prices.get_group(group))
        price_std = np.std(airbnb_districts_prices.get_group(group))
        price_skew = skew(airbnb_districts_prices.get_group(group))
        
        stats = [price_n_of_observations, price_mean, price_median,
                 price_std, price_skew]
   
            
        if price_skew >= 5:
            face_color = "#DE9C12"
            
        else:
            face_color = "#02b72e"
        
        i += 1
   
        ax = fig_3.add_subplot(13,3,i)
   
        sns.distplot(airbnb_districts_prices.get_group(group),
                     ax = ax,
                     color = face_color,
                     hist_kws = {
                         "edgecolor" : "black",
                         "alpha" : 0.6},
                     kde = False)
               
        ax.set_xlabel("Price",
              fontfamily = "Arial",
              fontsize = 16,
              fontweight = "bold")
                
        if i in [1,22,37]:
            ax.set_ylabel("Count",
                  fontfamily = "Arial",
                  fontsize = 16,
                  fontweight = "bold")
   
        ax.set_title(group,
                     loc = "right",
                     x = 1,
                     y = 0.75,
                     color = "black",
                     fontfamily = "Arial",
                     fontsize = 14,
                     fontweight = "bold")
        
        j = 0
        y = .70
        stat_headings = ["Observations", "Mean", "Median", "STDev", "Skew"]
        for stat in stats:
            ax.annotate(s = "{} = {:.2f}".format(stat_headings[j],stat),
                    xy = (.7, y),
                    xycoords=ax.transAxes,
                    color = "black",
                    weight = "bold",
                    fontsize = 10)
            y -= 0.125
            j += 1
            
    fig_3.suptitle("The distribution of normalized Airbnb rental prices per district.",
       x = 0.50,
       y = 0.90,
       horizontalalignment = "center",
       fontfamily = "Arial",
       fontsize = 18,
       fontweight = "bold",)
            
#%% --- Visualization Four: Small multiples histogram for Airbnb price data
# faceted by district

with plt.style.context('matplotlib_stylesheet_ejg_fixes'):

    # --- Create figure and axes ---
    i = 0
   
    fig_4 = plt.figure(figsize = (25.00, 25.00))
   
    for group in airbnb_districts_prices_normalized.groups:
        
        price_n_of_observations = len(airbnb_districts_prices_normalized.get_group(group))
        price_mean = np.mean(airbnb_districts_prices_normalized.get_group(group))
        price_median = np.median(airbnb_districts_prices_normalized.get_group(group))
        price_std = np.std(airbnb_districts_prices_normalized.get_group(group))
        price_skew = skew(airbnb_districts_prices_normalized.get_group(group))
        
        stats = [price_n_of_observations, price_mean, price_median,
                 price_std, price_skew]
   
            
        if price_skew >= 5:
            face_color = "#DE9C12"
            
        else:
            face_color = "#02b72e"
        
        i += 1
   
        ax = fig_4.add_subplot(13,3,i)
   
        sns.distplot(airbnb_districts_prices_normalized.get_group(group),
                     ax = ax,
                     color = face_color,
                     hist_kws = {
                         "edgecolor" : "black",
                         "alpha" : 0.6},
                     kde = False)
               
        ax.set_xlabel("Price",
              fontfamily = "Arial",
              fontsize = 16,
              fontweight = "bold")
                
        if i in [1,22,37]:
            ax.set_ylabel("Count",
                  fontfamily = "Arial",
                  fontsize = 16,
                  fontweight = "bold")
   
        ax.set_title(group,
                     loc = "right",
                     x = 1,
                     y = 0.75,
                     color = "black",
                     fontfamily = "Arial",
                     fontsize = 14,
                     fontweight = "bold")
        
        j = 0
        y = .70
        stat_headings = ["Observations", "Mean", "Median", "STDev", "Skew"]
        for stat in stats:
            ax.annotate(s = "{} = {:.2f}".format(stat_headings[j],stat),
                    xy = (.7, y),
                    xycoords=ax.transAxes,
                    color = "black",
                    weight = "bold",
                    fontsize = 10)
            y -= 0.125
            j += 1
            
        fig_4.suptitle("The distribution of normalized Airbnb rental prices per district.",
           x = 0.50,
           y = 0.90,
           horizontalalignment = "center",
           fontfamily = "Arial",
           fontsize = 18,
           fontweight = "bold",)
        
#%% --- Export Figures ---

current_filename_split = os.path.basename(__file__).split(".")[0].split("_")
current_filename_complete = "_".join(current_filename_split)

mkdir_path = Path("../../media/figures/raw/{}".format(current_filename_complete))
os.mkdir(mkdir_path)

figures = [fig_1, fig_2, fig_3, fig_4]
filenames = ["single_raw", "single_normalized", "multiple_raw", "multiple_normalized"]
file_extensions = [".png", ".svg"]

for figure, filename in zip(figures, filenames):
    for file_extension in file_extensions:
        filename_extended = filename + file_extension
        export_fp = Path.joinpath(mkdir_path, filename_extended)
        figure.savefig(export_fp,
                        dpi = 300,
                        bbox_inches = "tight")
             