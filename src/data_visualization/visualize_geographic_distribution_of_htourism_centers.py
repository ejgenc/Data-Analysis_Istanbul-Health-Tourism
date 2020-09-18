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
import matplotlib.colors as col
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import contextily as ctx #Used in conjuction with matplotlib/geopandas to set a basemap
from src.helper_functions import data_visualization_helper_functions as viz_helpers
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

with plt.style.context('matplotlib_stylesheet_ejg_fixes'):
    
    # --- Create Figure and Axes ---
    fig_1 = plt.figure(figsize = (19.20,19.20))
    ax = fig_1.add_subplot(1,1,1)
            
    # --- Choropleth Map ---
    htourism_gdf_agg.plot(ax = ax,
                          column = "htourism_c",
                          edgecolor = "black",
                          alpha = 1,
                          cmap = "Oranges",
                          missing_kwds = {
                              "color" : "white",
                              "alpha" : 0.5,
                              "hatch" : "//",
                              "label" : "No institution"}
                          )
    
    # --- Set Basemap ---
    ctx.add_basemap(ax, zoom = 11,
                crs = htourism_gdf_agg.crs,
                source = ctx.providers.Esri.WorldGrayCanvas)
    
    
    # --- Text and Labels ---
    # --- Label some districts ---
    districts_to_label_list = ["Silivri", "Catalca", "Buyukcekmece", "Arnavutkoy", "Eyupsultan", "Sariyer",
                           "Beykoz", "Sile", "Cekmekoy", "Tuzla", "Pendik", "Maltepe", "Basaksehir"]
    viz_helpers.label_district_on_map(ax, htourism_gdf_agg, "district_e", districts_to_label_list)
    
    # --- Legend ---
    # --- Color Map ---
    oranges_cmap = cm.ScalarMappable(col.Normalize(0, max(htourism_gdf_agg["htourism_c"].values)), cm.Oranges)
    viz_helpers.create_cmap_legend_in_figure(ax = ax,
                                             cmap_object = oranges_cmap,
                                             label = "Health tourism related institution count per district",
                                             label_size = 12,
                                             label_weight = "bold")
    
    # --- Plot wide fixes and fine-tuning ---
    # --- Axis fixes ---
    ax.set_axis_off()
    
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
    districts_to_label_list = ["Silivri", "Catalca", "Buyukcekmece", "Arnavutkoy", "Eyupsultan", "Sariyer",
                           "Beykoz", "Sile", "Cekmekoy", "Tuzla", "Pendik", "Maltepe", "Basaksehir"]
    viz_helpers.label_district_on_map(ax, htourism_gdf_agg, "district_e", districts_to_label_list)

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
                          cmap = "Oranges",
                          missing_kwds = {
                              "color" : "white",
                              "alpha" : 0.5,
                              "hatch" : "//"})
    
    # Label some districts
    districts_to_label_list = ["Silivri", "Catalca", "Buyukcekmece", "Arnavutkoy", "Eyupsultan", "Sariyer",
                           "Beykoz", "Sile", "Cekmekoy", "Tuzla", "Pendik", "Maltepe", "Basaksehir"]
    viz_helpers.label_district_on_map(ax_1, htourism_gdf_agg, "district_e", districts_to_label_list)
    
    # --- Legend ---
    # --- Color Map ---
    oranges_cmap = cm.ScalarMappable(col.Normalize(0, max(htourism_gdf_agg["htourism_c"].values)), cm.Oranges)
    viz_helpers.create_cmap_legend_in_figure(ax = ax_1,
                                             cmap_object = oranges_cmap,
                                             label = "Health tourism related institution count per district",
                                             label_size = 12,
                                             label_weight = "bold")
    
    # --- Symbol Map ---
    
    #Plot actual data
    htourism_gdf_raw.plot(ax = ax_2,
                    color = color_orange,
                    zorder = 3,
                    alpha = 0.85,
                    markersize = 120,
                    marker = "^",
                    edgecolor = "black")
    
    #Plot district backgrounds
    htourism_gdf_agg.plot(ax = ax_2,
                          edgecolor = "black",
                          alpha = 0.5,
                          color = "white")
    
    # Label some districts
    viz_helpers.label_district_on_map(ax_2, htourism_gdf_agg, "district_e", districts_to_label_list)
     
    
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

mkdir_path = Path("../../media/figures/raw/{}".format(current_filename_complete))
os.mkdir(mkdir_path)

figures = [fig_1, fig_2, fig_3]
filenames = ["choropleth", "actual", "combined"]
file_extensions = [".png", ".svg"]

for figure, filename in zip(figures, filenames):
    for file_extension in file_extensions:
        filename_extended = filename + file_extension
        export_fp = Path.joinpath(mkdir_path, filename_extended)
        figure.savefig(export_fp,
                        dpi = (lambda x: 300 if file_extension == ".png" else 1200)(file_extension),
                        bbox_inches = "tight",
                        pad_inches = 0)