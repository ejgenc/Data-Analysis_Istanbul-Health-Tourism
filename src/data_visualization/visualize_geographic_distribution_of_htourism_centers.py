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
from numpy import arange
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as col
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
    
#%% --- Visualization Four : Choropleth Map + Distribution + Vertical Bar Chart

with plt.style.context('matplotlib_stylesheet_ejg_fixes'):
    
    
    # --- Create figure and axes ---
    fig_4 = plt.figure(figsize = (19.20,19.20))
    
    gs = fig_4.add_gridspec(2,8,
                            figure = fig_4,
                            top = 0.50, bottom = 0,
                            wspace = 0, hspace = 0)
    
    ax_1 = fig_4.add_subplot(gs[0,:-1])
    ax_2 = fig_4.add_subplot(gs[1,:-1])
    ax_3 = fig_4.add_subplot(gs[:,-1:])
                
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
    
    # --- Text ---
    
    # ax title
    ax_1.text(x = 0.005, y = 0.885,
              s = "Distribution of health tourism related institutions \nat the district level.",
              fontdict = viz_helpers.font_title,
              transform = ax_1.transAxes)
    
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
                                              label_size = 14,
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
    
    # --- Text ---
    
    # ax title
    ax_2.text(x = 0.005, y = 0.885,
              s = "Distribution of health tourism related institutions \nacross Istanbul.",
              fontdict = viz_helpers.font_title,
              transform = ax_2.transAxes)
    
    # Label some districts
    viz_helpers.label_district_on_map(ax_2, htourism_gdf_agg, "district_e", districts_to_label_list)
    
    # --- Bar Plot ---
    
    # --- prepare data ---
    bar_widths = htourism_gdf_agg["htourism_c"].sort_values(ascending = False).fillna(0).astype(int).values
    bar_labels =  htourism_gdf_agg.sort_values(by = "htourism_c", ascending = False).fillna(0)["district_e"].values
    bar_positions = arange(len(bar_labels))
    
    # --- plot data ---
    ax_3.barh(bar_positions, bar_widths,
        align = "center",
        height = 0.85,
        color = oranges_cmap.to_rgba(bar_widths),
        edgecolor = "black")
    
    # --- Spines and Axes ---
    # --- set spines ---
    ax_3.spines["top"].set_visible(True)
    ax_3.spines["bottom"].set_visible(False)
    ax_3.spines["right"].set_visible(True)
    ax_3.spines["left"].set_visible(False)
    
    # --- invert axes for left/top align ---
    ax_3.invert_xaxis()
    ax_3.invert_yaxis()
    
    # --- Ticks and Labels ---
    # --- deal with tick positions ---
    ax_3.set_xticks([0,10,20,30])
    ax_3.xaxis.tick_top()
    ax_3.xaxis.set_label_position('top') 
    ax_3.yaxis.tick_right()
    ax_3.set_yticks(bar_positions)
    
    # --- deal with tick positions ---
    #Setting y-tick labels and positions
    ax_3.set_yticklabels(bar_labels)
    ax_3.yaxis.set_label_position("right")
    
    # --- add value labels ---
    viz_helpers.add_value_labels_barh(ax_3, 5, fontsize = 14)

    # --- set facecolor ---
    ax_3.set_facecolor("#D0CFD4")
    
        
    # --- Plot wide fixes and fine-tuning ---
    # --- Axis fixes ---
    for ax in [ax_1,ax_2]:
        ax.get_xaxis().set_ticks([])
        ax.get_yaxis().set_ticks([])
        ax.spines["top"].set_visible(True)
        ax.spines["bottom"].set_visible(True)
        ax.spines["left"].set_visible(True)
        ax.spines["right"].set_visible(True)
    
    # --- Set basemap for all axes --- 
    for ax in [ax_1,ax_2]:
        ctx.add_basemap(ax, zoom = 11,
                    crs = htourism_gdf_agg.crs,
                    source = ctx.providers.Esri.WorldGrayCanvas)
    
    # --- Set facecolor to match basemap background color ---
    fig_4.set_facecolor("#D0CFD4")
        
    # --- Tight layout just for good measure
    plt.tight_layout()
    
#%% --- Export Figures ---

current_filename_split = os.path.basename(__file__).split("_")[:-1]
current_filename_complete = "_".join(current_filename_split)

mkdir_path = Path("../../media/figures/raw/{}".format(current_filename_complete))
os.mkdir(mkdir_path)

figures = [fig_1, fig_2, fig_3, fig_4]
filenames = ["choropleth", "actual", "two_maps", "maps_barchart"]
file_extensions = [".png", ".svg"]

for figure, filename in zip(figures, filenames):
    for file_extension in file_extensions:
        filename_extended = filename + file_extension
        export_fp = Path.joinpath(mkdir_path, filename_extended)
        figure.savefig(export_fp,
                        dpi = (lambda x: 300 if file_extension == ".png" else 1200)(file_extension),
                        bbox_inches = "tight",
                        facecolor = "#D0CFD4",
                        pad_inches = 0)