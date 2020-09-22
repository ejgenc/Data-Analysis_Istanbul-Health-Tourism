# -*- coding: utf-8 -*-
"""
------ What is this file? ------

This script targets one file:
    - geographic_distribution_of_htourism_centers.shp
    
The script produces a small-multiples scatterplot visualization of htourism center count
per distict.

Returns a small multiples view of two scatterplots related to htourism center
count at district level.
"""
#%% --- Import Required Packages ---

import os
from pathlib import Path # To wrap around filepaths
import geopandas as gpd
from scipy.stats import pearsonr
import matplotlib.pyplot as plt

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Import Data ---

#Import htourism centers data - aggregated at the district level
import_fp = Path("../../data/final/geographic_distribution_of_htourism_centers.shp")
htourism_gdf_agg = gpd.read_file(import_fp, encoding = "utf-8-sig")

#%% --- Fill missing values with zero ---

htourism_gdf_agg.fillna(0, inplace = True)

#%% --- Get pearson's r ---

results = []
dependent_variable = htourism_gdf_agg.loc[:,"htourism_c"]
independent_variables = [htourism_gdf_agg.loc[:,"population"],
                         htourism_gdf_agg.loc[:,"yearly_ave"]]
labels = ["Population", "Yearly average household income (in thousand TL)"]

for independent_variable in independent_variables:
    result = pearsonr(independent_variable, dependent_variable)
    results.append(result)
    
    
#%% --- Visualization One: Small multiples scatterplot

with plt.style.context('matplotlib_stylesheet_ejg_fixes'):
    
    # --- Create figure and axes ---
    fig_1 = plt.figure(figsize = (10.80,10.80))
    
    i = 1
    for independent_variable in independent_variables:
        ax = fig_1.add_subplot(2,1,i)
        i += 1
        ax.scatter(independent_variable, dependent_variable,
                   s = 40,
                   color = "#02b72e",
                   marker = "s")
        
        ax.set_xlabel(labels[i -2],
                      fontfamily = "Arial",
                      fontsize = 16,
                      fontweight = "bold")
        
        ax.text(x = 0.90, y = 0.90,
              s = "r = {:.2f}".format(results[i - 2][0]),
              transform = ax.transAxes,
              fontfamily = "Arial",
              fontsize = 14,
              fontweight = "bold")
        
    fig_1.text(x = 0.05, y = 0.225,
              s = "Number of institutions related to health tourism",
              fontfamily = "Arial",
              fontsize = 16,
              fontweight = "bold",
              rotation = 90)
#%% --- Export Figures ---

current_filename_split = os.path.basename(__file__).split(".")[0].split("_")
current_filename_complete = "_".join(current_filename_split)

mkdir_path = Path("../../media/figures/raw/{}".format(current_filename_complete))
os.mkdir(mkdir_path)

file_extensions = [".png", ".svg"]

for file_extension in file_extensions:
    filename_extended = "scatterplot" + file_extension
    export_fp = Path.joinpath(mkdir_path, filename_extended)
    fig_1.savefig(export_fp,
                    bbox_inches = "tight")