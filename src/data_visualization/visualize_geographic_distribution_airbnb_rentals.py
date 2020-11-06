# -*- coding: utf-8 -*-
"""
------ What is this file? ------

This script targets two files:
    - istanbul_airbnb_processed_shapefile.shp
    - geographic_distribution_of_airbnb_rentals.shp
    
The script visualizes the geographic distribution of airbnb rentals at
the district level and at the individual center level. 

Returns a data visualization that represents the geographic
distribution of airbnb rental. The visualization is a combined view of
a choropleth map, a symbol map and a horizontal bar chart.
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

#Import airbnb rentals data - raw
import_fp = Path("../../data/processed/istanbul_airbnb_processed_shapefile.shp")
airbnb_gdf_raw = gpd.read_file(import_fp, encoding = "utf-8-sig")

#Import htourism centers data - aggregated at the district level
import_fp = Path("../../data/final/geographic_distribution_of_airbnb_rentals.shp")
airbnb_gdf_agg = gpd.read_file(import_fp, encoding = "utf-8-sig")

#%% --- Define universal variables (color, typography etc.)

color_lblue = "#1CB2FE"

#%% --- Visualization One : Choropleth Map + Distribution + Horizontal Bar Chart

with plt.style.context('matplotlib_stylesheet_ejg_fixes'):
    
    # --- Create figure and axes ---
    fig_1 = plt.figure(figsize = (19.20,19.20))
    
    gs = fig_1.add_gridspec(2,8,
                            figure = fig_1,
                            top = 0.50, bottom = 0,
                            wspace = 0, hspace = 0)
    
    ax_1 = fig_1.add_subplot(gs[0,:-1])
    ax_2 = fig_1.add_subplot(gs[1,:-1])
    ax_3 = fig_1.add_subplot(gs[:,-1:])
                
    # --- Choropleth Map --- 
    
    # Plot actual data
    airbnb_gdf_agg.plot(ax = ax_1,
                          column = "airbnb_cou",
                          edgecolor = "black",
                          alpha = 1,
                          cmap = "Blues")
    
    # --- Text ---
    
    # ax title
    ax_1.text(x = 0.005, y = 0.93,
              s = "Distribution of Airbnb rentals at the district level.",
              fontdict = viz_helpers.font_title,
              transform = ax_1.transAxes)
    
    # Label some districts
    districts_to_label_list = ["Silivri", "Catalca", "Buyukcekmece", "Arnavutkoy", "Eyupsultan", "Sariyer",
                            "Beykoz", "Sile", "Cekmekoy", "Tuzla", "Pendik", "Maltepe", "Basaksehir"]
    viz_helpers.label_district_on_map(ax_1, airbnb_gdf_agg, "district_e", districts_to_label_list)
    
    # --- Legend ---
    # --- Color Map ---
    blues_cmap = cm.ScalarMappable(col.Normalize(0, max(airbnb_gdf_agg["airbnb_cou"].values)), cm.Blues)
    viz_helpers.create_cmap_legend_in_figure(ax = ax_1,
                                              cmap_object = blues_cmap,
                                              label = "Airbnb rental count per district",
                                              label_size = 14,
                                              label_weight = "bold")
    
    # --- Symbol Map ---
    
    #Plot actual data
    airbnb_gdf_raw.plot(ax = ax_2,
                    color = color_lblue,
                    zorder = 3,
                    alpha = 0.65,
                    markersize = 120,
                    marker = "o",
                    edgecolor = "black")
    
    #Plot district backgrounds
    airbnb_gdf_agg.plot(ax = ax_2,
                          edgecolor = "black",
                          alpha = 0.5,
                          color = "white")
    
    # --- Text ---
    
    # ax title
    ax_2.text(x = 0.005, y = 0.93,
              s = "Distribution of Airbnb rentals across Istanbul.",
              fontdict = viz_helpers.font_title,
              transform = ax_2.transAxes)
    
    # Label some districts
    viz_helpers.label_district_on_map(ax_2, airbnb_gdf_agg, "district_e", districts_to_label_list)
    
    # --- Bar Plot ---
    
    # --- prepare data ---
    bar_widths = airbnb_gdf_agg["airbnb_cou"].sort_values(ascending = False).fillna(0).astype(int).values
    bar_labels =  airbnb_gdf_agg.sort_values(by = "airbnb_cou", ascending = False).fillna(0)["district_e"].values
    bar_positions = arange(len(bar_labels))
    
    # --- plot data ---
    ax_3.barh(bar_positions, bar_widths,
        align = "center",
        height = 0.85,
        color = blues_cmap.to_rgba(bar_widths),
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
    ax_3.set_xticks([0,2500,5000])
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
                    crs = airbnb_gdf_agg.crs,
                    source = ctx.providers.Esri.WorldGrayCanvas)
    
    # --- Set facecolor to match basemap background color ---
    fig_1.set_facecolor("#D0CFD4")
        
    # --- Tight layout just for good measure
    plt.tight_layout()
    
#%% --- Export Figures ---

current_filename_split = os.path.basename(__file__).split("_")[:-1]
current_filename_complete = "_".join(current_filename_split)

mkdir_path = Path("../../media/figures/raw/{}".format(current_filename_complete))
os.mkdir(mkdir_path)

figure = fig_1
filename = "maps_barchart_g1"
file_extensions = [".png", ".svg"]

for file_extension in file_extensions:
    filename_extended = filename + file_extension
    export_fp = Path.joinpath(mkdir_path, filename_extended)
    figure.savefig(export_fp,
                    dpi = (lambda x: 300 if file_extension == ".png" else 600)(file_extension),
                    bbox_inches = "tight",
                    facecolor = "#D0CFD4",
                    pad_inches = 0)

