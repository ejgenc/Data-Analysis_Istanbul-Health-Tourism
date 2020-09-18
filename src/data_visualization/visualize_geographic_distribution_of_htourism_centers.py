# -*- coding: utf-8 -*-
"""
------ What is this file? ------

This script targets two files:
    - htourism_centers_processed.shp
    - istanbul_districts.shp
    
The script visualizes the geographic distribution of health tourism centers at
the district level and at the individual center level. 

Returns 
"""
#%% --- Import Required Packages ---

import os
from pathlib import Path # To wrap around filepaths
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import contextily as ctx #Used in conjuction with matplotlib/geopandas to set a basemap
#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Import Data ---

#Import htourism centers data - raw
import_fp = Path("../../data/processed/htourism_centers_processed.shp")
htourism_gdf_raw = gpd.read_file(import_fp, encoding = "utf-8-sig")

#Import htourism centers data - aggregated at the district level
import_fp = Path("../../data/final/geographic_distribution_of_htourism_centers.shp")
htourism_gdf_agg = gpd.read_file(import_fp, encoding = "utf-8-sig")

#%% --- Define universal variables (color, typography etc.)

color_orange = "#F68C69"

#%% --- Visualization One: Choropleth map of htourism centers per district ---

# Initialize stylesheet
with plt.style.context('matplotlib_stylesheet_ejg_fixes'):
    
    # Create a figure and corresponding axes
    fig_1 = plt.figure(figsize = (19.20,19.20))
    ax = fig_1.add_subplot(1,1,1)
    
    #Axis fixes
    ax.set_axis_off()
    
    #Plot actual data
    htourism_gdf_agg.plot(ax = ax,
                          column = "htourism_c",
                          edgecolor = "black",
                          alpha = 1,
                          cmap = "Oranges")
    
    #Get basemap
    ctx.add_basemap(ax, zoom = 11,
                crs = htourism_gdf_agg.crs,
                source = ctx.providers.Esri.WorldGrayCanvas)
    
    # Label some districts
    
#%% --- Visualization Two: Distribution of htourism centers ---

with plt.style.context('matplotlib_stylesheet_ejg_fixes'):
    
    # Create a figure and corresponding axes
    fig_2 = plt.figure(figsize = (19.20,19.20))
    ax = fig_2.add_subplot(1,1,1)
    
    #Axis fixes
    
    ax.set_axis_off()
    
    #Plot actual data
    htourism_gdf_raw.plot(ax = ax,
                    color = color_orange,
                    zorder = 3,
                    alpha = 0.85,
                    markersize = 90,
                    marker = "^",
                    edgecolor = "black")
    
    #Plot district backgrounds
    htourism_gdf_agg.plot(ax = ax,
                          edgecolor = "black",
                          alpha = 0.5,
                          color = "white")
    
    #Get basemap
    ctx.add_basemap(ax, zoom = 11,
                crs = htourism_gdf_agg.crs,
                source = ctx.providers.Esri.WorldGrayCanvas)
    
    
    # Label some districts

#%% --- Visualization Three: Choropleth map + distribution ---

with plt.style.context('matplotlib_stylesheet_ejg_fixes'):
    
    
    # --- Create figure and axes ---
    fig_3 = plt.figure(figsize = (19.20,19.20))
    
    ax_1 = fig_3.add_subplot(2,1,1)
    ax_2 = fig_3.add_subplot(2,1,2)
                
    # --- Choropleth Map --- 
    
    # Plot actual data
    htourism_gdf_agg.plot(ax = ax_1,
                          column = "htourism_c",
                          edgecolor = "black",
                          alpha = 1,
                          cmap = "Oranges")

    # Label some districts
    
    # --- Symbol Map ---
    
    #Plot actual data
    htourism_gdf_raw.plot(ax = ax_2,
                    color = color_orange,
                    zorder = 3,
                    alpha = 0.85,
                    markersize = 90,
                    marker = "^",
                    edgecolor = "black")
    
    #Plot district backgrounds
    htourism_gdf_agg.plot(ax = ax_2,
                          edgecolor = "black",
                          alpha = 0.5,
                          color = "white")
    
     # Label some districts
     
    
    # --- Plot wide fixes and fine-tuning ---
    
    # --- Axis fixes ---
    for ax in [ax_1,ax_2]:
        ax.set_axis_off()
        
    # --- Set basemap for all axes --- 
    for ax in [ax_1,ax_2]:
        ctx.add_basemap(ax, zoom = 11,
                    crs = htourism_gdf_agg.crs,
                    source = ctx.providers.Esri.WorldGrayCanvas)
        
    # --- Adjust Spacing ---
    plt.tight_layout()
    plt.subplots_adjust(hspace = -0.28)
    
#%% --- Export Figures ---

current_filename_split = os.path.basename(__file__).split("_")[:-1]
current_filename_complete = "_".join(current_filename_split)

mkdir_path = Path("../../media/figures/{}".format(current_filename_complete))
os.mkdir(mkdir_path)

filenames = ["choropleth", "actual", "combined"]
figures = [fig_1, fig_2, fig_3]

for filename, figure in zip(filenames, figures):
    filename = filename + ".png"
    export_fp = Path.joinpath(mkdir_path, filename)
    figure.savefig(export_fp,
                   format = "png",
                   dpi = 1200,
                   bbox_inches = "tight",
                   pad_inches = 0)
    