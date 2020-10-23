# -*- coding: utf-8 -*-
"""
------ What is this file? ------

This script targets one file:
    - geographic_distribution_of_airbnb_rentals.shp
    
The script produces a small-multiples scatterplot visualization of airbnb rental count
per distict.

Returns a small multiples view of two scatterplots related to airbnb rental
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

#Import airbnb rentals data - aggregated at the district level
import_fp = Path("../../data/final/geographic_distribution_of_airbnb_rentals.shp")
airbnb_rentals_agg = gpd.read_file(import_fp, encoding = "utf-8-sig")

#%% --- Get pearson's r ---

results = []
dependent_variable = airbnb_rentals_agg.loc[:,"airbnb_cou"]
independent_variables = [airbnb_rentals_agg.loc[:,"population"],
                         airbnb_rentals_agg.loc[:,"yearly_ave"]]

for independent_variable in independent_variables:
    result = pearsonr(independent_variable, dependent_variable)
    results.append(result)
    
#%% --- Visualization One: Small multiples scatterplot

with plt.style.context('matplotlib_stylesheet_ejg_fixes'):
    
    # --- Create figure and axes ---
    fig_1 = plt.figure(figsize = (10.80,10.80))
    
    districts_to_label_list = [
                          ["Esenyurt", "Kucukcekmece", "Bahcelievler",
                           "Uskudar", "Kadikoy", "Besiktas",
                           "Sisli", "Bakirkoy", "Beyoglu", "Fatih"],
                          ["Kadikoy","Besiktas", "Bakirkoy","Adalar",
                           "Sisli", "Sariyer","Uskudar",
                           "Fatih", "Beyoglu"]
                          ]
    labels = ["Population", "Yearly average household income (in thousand TL)"]
    

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
        
        ax.get_xaxis().get_major_formatter().set_scientific(False) #Turn off scientific notation on x axis
        
        districts_to_label = (lambda x: districts_to_label_list[0] if np.array_equal(independent_variable,airbnb_rentals_agg.loc[:,"population"]) else districts_to_label_list[1])(independent_variable)
        districts_to_label_mask = airbnb_rentals_agg.loc[:,"district_e"].isin(districts_to_label)

        districts_to_label_xy_df = airbnb_rentals_agg.loc[districts_to_label_mask,["district_e","airbnb_cou","population","yearly_ave"]]
    
        for idx, row in districts_to_label_xy_df.iterrows():
            x = (lambda x: row["yearly_ave"] + 2 if np.array_equal(independent_variable,airbnb_rentals_agg.loc[:,"yearly_ave"]) else row["population"] + 3)(independent_variable)
            y = row["airbnb_cou"] #To align it properly
            ax.annotate(s = row["district_e"],
                          xy = (x,y),
                          horizontalalignment='left',
                          verticalalignment = "center")
        
    fig_1.text(x = 0.05, y = 0.40,
              s = "Number of Airbnb rentals",
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

    

