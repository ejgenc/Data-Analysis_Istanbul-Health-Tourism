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
import numpy as np

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
    
    districts_to_label_list = [
                          ["Esenyurt", "Kucukcekmece", "Bahcelievler",
                           "Uskudar", "Kadikoy", "Atasehir", "Besiktas",
                           "Sisli", "Bakirkoy", "Beyoglu", "Fatih"],
                          ["Kadikoy","Besiktas", "Bakirkoy","Adalar",
                           "Sisli", "Sariyer","Uskudar","Atasehir",
                           "Maltepe","Fatih", "Beyoglu","Bahcelievler"]
                          ]

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
        
        districts_to_label = (lambda x: districts_to_label_list[0] if np.array_equal(independent_variable,htourism_gdf_agg.loc[:,"population"]) else districts_to_label_list[1])(independent_variable)
        districts_to_label_mask = htourism_gdf_agg.loc[:,"district_e"].isin(districts_to_label)

        districts_to_label_xy_df = htourism_gdf_agg.loc[districts_to_label_mask,["district_e","htourism_c","population","yearly_ave"]]
    
        for idx, row in districts_to_label_xy_df.iterrows():
            x = (lambda x: row["yearly_ave"] + 2 if np.array_equal(independent_variable,htourism_gdf_agg.loc[:,"yearly_ave"]) else row["population"] + 3)(independent_variable)
            y = row["htourism_c"] #To align it properly
            ax.annotate(s = row["district_e"],
                          xy = (x,y),
                          horizontalalignment='left',
                          verticalalignment = "center")
        
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