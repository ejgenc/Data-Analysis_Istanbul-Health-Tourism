# -*- coding: utf-8 -*-
"""
------ What is this file? ------

This script targets one file:
    - distance_price_dataset.shp
    
The script produces scatterplots that show Pearson'r and Spearman's rho
analysis results for multiple subsets of the distance_price datasets
The relations are calculated to see whether closeness
to a health tourism center affects price in some way.

Returns multiple scatterplots,both single and small-multiples

"""
#%% --- Import Required Packages ---

import os
from pathlib import Path # To wrap around filepaths
import geopandas as gpd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr,spearmanr,iqr

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Import data ---

import_fp = Path("../../data/final/distance_price_dataset.shp")
distance_price = gpd.read_file(import_fp)

#%% --- Create subsets of the dataset for visualization ---

# --- Prices within +/- 1.5 IQR ---

#Calculate iqr, q1 and q3 for price
price_iqr = iqr(distance_price["price"], axis = 0)
q1 = distance_price["price"].quantile(0.25)
q3 = distance_price["price"].quantile(0.75)

#Create masks to select values only within +/- 1.5 IQR
min_mask = distance_price["price"] >= q1 - (price_iqr * 1.5)
max_mask = distance_price["price"] <= q3 + (price_iqr * 1.5)
combined_mask = min_mask & max_mask

#Subset the dataset with the mask above
distance_price_normalized = distance_price[combined_mask]

# --- Prices for selected districts: Sisli, Besiktas, Kadıkoy, Atasehir, Uskudar ---
# !!! IMPORTANT NOTE: These districts are top 5 in health tourism center count

selected_districts = ["Sisli", "Besiktas", "Kadikoy",
                      "Atasehir", "Uskudar"]

#Create an empty dictionary for district name and values
distance_price_per_district= {}

#Loop over selected districts, create a mask and select for each of them
for district in selected_districts:
    district_mask = distance_price_normalized["district_e"] == district
    selection = distance_price_normalized.loc[district_mask,:]
    distance_price_per_district[district] = selection

#%% --- Visualizations ---

#%% --- Visualization One: Scatterplot for raw distance_price ---

with plt.style.context('matplotlib_stylesheet_ejg_fixes'):
    
    # --- Calculate pearson's r and spearman's rho
    r = pearsonr(distance_price["distance_i"],distance_price["price"])[0]
    rho = spearmanr(distance_price["distance_i"],distance_price["price"])[0]
    
    # --- Create figure and axes ---
    fig_1 = plt.figure(figsize = (10.80,10.80))
    
    ax = fig_1.add_subplot(1,1,1)
    
    # --- Plot the data ---
    ax.scatter(distance_price["distance_i"],
               distance_price["price"],
               s = 80,
               alpha = 0.80,
               color = "#1CB2FE",
               marker = "o",
               edgecolor = "black")  
    
    # --- Labels ---
    
    ax.set_xlabel("Distance to nearest health tourism related institution (meters)",
              fontfamily = "Arial",
              fontsize = 16,
              fontweight = "bold")
    
    ax.set_ylabel("Price",
          fontfamily = "Arial",
          fontsize = 16,
          fontweight = "bold")
    
    # --- Annotation ---
    
    ax.text(x = 0.85, y = 0.95,
      s = "r = {:.2f}".format(r),
      transform = ax.transAxes,
      fontfamily = "Arial",
      fontsize = 18,
      fontweight = "bold")
    
    ax.text(x = 0.85, y = 0.90,
      s = "rho = {:.2f}".format(rho),
      transform = ax.transAxes,
      fontfamily = "Arial",
      fontsize = 18,
      fontweight = "bold")
    
    fig_1.suptitle(("Scatterplot of Airbnb rents and\n distance "
                    "to nearest health-tourism related institution"),
               x = 0.50,
               y = 0.92,
               horizontalalignment = "center",
               fontfamily = "Arial",
               fontsize = 18,
               fontweight = "bold",)
    
#%% --- Visualization two: Scatterplot for distance_price_normalized ---

with plt.style.context('matplotlib_stylesheet_ejg_fixes'):
    
    # --- Calculate pearson's r and spearman's rho
    r = pearsonr(distance_price_normalized["distance_i"],
                 distance_price_normalized["price"])[0]
    rho = spearmanr(distance_price_normalized["distance_i"],
                    distance_price_normalized["price"])[0]
    
    # --- Create figure and axes ---
    fig_2 = plt.figure(figsize = (10.80,10.80))
    
    ax = fig_2.add_subplot(1,1,1)
    
    # --- Plot the data ---
    ax.scatter(distance_price_normalized["distance_i"],
               distance_price_normalized["price"],
               s = 80,
               alpha = 0.80,
               color = "#1CB2FE",
               marker = "o",
               edgecolor = "black")  
    
    # --- Labels ---
    
    ax.set_xlabel("Distance to nearest health tourism related institution (meters)",
              fontfamily = "Arial",
              fontsize = 16,
              fontweight = "bold")
    
    ax.set_ylabel("Price",
          fontfamily = "Arial",
          fontsize = 16,
          fontweight = "bold")
    
    # --- Annotation ---
    
    ax.text(x = 0.85, y = 0.95,
      s = "r = {:.2f}".format(r),
      transform = ax.transAxes,
      fontfamily = "Arial",
      fontsize = 18,
      fontweight = "bold")
    
    ax.text(x = 0.85, y = 0.90,
      s = "rho = {:.2f}".format(rho),
      transform = ax.transAxes,
      fontfamily = "Arial",
      fontsize = 18,
      fontweight = "bold")
    
    fig_2.suptitle(("Scatterplot of normalized Airbnb rents and\n distance "
                    "to nearest health-tourism related institution"),
               x = 0.50,
               y = 0.92,
               horizontalalignment = "center",
               fontfamily = "Arial",
               fontsize = 18,
               fontweight = "bold",)
    
#%% --- Visualization Three: Small-multiples scatterplot per district ---

with plt.style.context('matplotlib_stylesheet_ejg_fixes'):
    
    # --- Create figure and axes ---
    
    fig_3 = plt.figure(figsize = (19.20,10.80))
    
    gs = fig_3.add_gridspec(ncols = 3,
                            nrows = 2,
                            figure = fig_3)
    # Ax 1 to ax 5 
    
    col = 0
    row = 1
    
    for district_name,district_gdf in distance_price_per_district.items():
        
        # --- Calculate pearson's r and spearman's rho
        r = pearsonr(district_gdf["distance_i"],
                     district_gdf["price"])[0]
        rho = spearmanr(district_gdf["distance_i"],
                        district_gdf["price"])[0]
        
        # --- Add axes and plot the Data ---
        ax = fig_3.add_subplot(gs[col, row])
        ax.scatter(district_gdf["distance_i"],
                   district_gdf["price"],
                   s = 80,
                   alpha = 0.80,
                   color = "#1CB2FE",
                   marker = "o",
                   edgecolor = "black")
        
        ax.set_xlabel("")
        
        # --- Label y-axis conditionally ---
        if (row == 1 and col == 0) or (row == 0 and col == 1):
            ax.set_ylabel("Price",
              fontfamily = "Arial",
              fontsize = 16,
              fontweight = "bold")
            
        ax.set_title(district_name,
                     fontfamily = "Arial",
                     fontsize = 18,
                     fontweight = "bold",)
        
        # --- Annotation ---
    
        ax.text(x = 0.50, y = 0.95,
          s = "r = {:.2f}".format(r),
          transform = ax.transAxes,
          fontfamily = "Arial",
          fontsize = 18,
          fontweight = "bold")
        
        ax.text(x = 0.50, y = 0.90,
          s = "rho = {:.2f}".format(rho),
          transform = ax.transAxes,
          fontfamily = "Arial",
          fontsize = 18,
          fontweight = "bold")
                
        
        if row == 2:
            row = 0
            col = 1
        else:
            row += 1
            
    fig_3.text(x = 0.33,
               y = 0.07,
               s = "Distance to nearest health tourism related institution (meters)",
               fontfamily = "Arial",
               fontsize = 18,
               fontweight = "bold")
            

#%% --- Export Figures ---

current_filename_split = os.path.basename(__file__).split(".")[0].split("_")
current_filename_complete = "_".join(current_filename_split)

mkdir_path = Path("../../media/figures/raw/{}".format(current_filename_complete))
os.mkdir(mkdir_path)

figures = [fig_1, fig_2, fig_3]
filenames = ["correlation_raw","correlation_normalized","correlation_multiple"]
file_extensions = [".png", ".svg"]

for figure, filename in zip(figures, filenames):
    for file_extension in file_extensions:
        filename_extended = filename + file_extension
        export_fp = Path.joinpath(mkdir_path, filename_extended)
        figure.savefig(export_fp,
                        dpi = 300,
                        bbox_inches = "tight")
