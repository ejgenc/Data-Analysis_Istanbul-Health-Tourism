# -*- coding: utf-8 -*-
"""
------ What is this file? ------

This script contains some helper functions that are used in the scripts
found under src/data_visualization.


"""

#%% --- Import required packages ---

import os
from shapely.geometry import LineString
import geopandas as gpd
import matplotlib.pyplot as plt
from src.helper_functions import data_analysis_helper_functions as functions_analysis

#%% --- DEFINITIONS ---

# Set font info
font_title = {'family': 'sans-serif',
              "fontname": "Arial",
              'color':  'black',
              'weight': 'bold',
              'size': 18}

#Gill Sans MT doesn't work for Turkish charset.
font_axislabels = {'family': 'sans-serif',
                   "fontname": "Arial",
                   'color':  'black',
                   'weight': 'bold',
                   'size': 20}

font_xticks = {'family': 'sans-serif', #Modified for this plot
                   "fontname": "Arial",
                   'color':  'black',
                   'weight': 'normal',
                   'size': 12}

font_yticks = {'family': 'sans-serif',
                   "fontname": "Arial",
                   'color':  'black',
                   'weight': 'normal',
                   'size': 16}

font_figtitle = {'family': 'sans-serif',
              "fontname": "Arial",
              'color':  'black',
              'weight': 'bold',
              'size': 90}

#%% --- FUNCTION : confirm_nearest_neighbor_analysis ---

#%% --- Subfunctions ---
def create_link_between_origin_and_nearest_geom(nn_analysis_gdf):
    valerror_text = "Argument nn_analysis_gdf should be of type geopandas.GeoDataFrame. Got {} ".format(type(nn_analysis_gdf))
    if functions_analysis.is_gdf(nn_analysis_gdf) is False:
        raise ValueError(valerror_text)
        
    attriberror_text = "Argument provided does not have geometry information."
    if functions_analysis.has_geometry(nn_analysis_gdf) is False:
        raise AttributeError(attriberror_text)
        
    attriberror_text = "nn_analysis_gdf object is missing crs information."
    if functions_analysis.has_crs(nn_analysis_gdf) is False:
        raise AttributeError(attriberror_text)
        
    links = [LineString([p1,p2]) for p1, p2 in nn_analysis_gdf.loc[:,["point_of_origin","nearest_point"]].values]

    links_gseries = gpd.GeoSeries(links,
                              crs = nn_analysis_gdf.crs)
    
    return links_gseries

def plot_nearest_neighbor_analysis(nn_analysis_gdf, link_gseries):
    valerror_text = "Argument nn_analysis_gdf should be of type geopandas.GeoDataFrame. Got {} ".format(type(nn_analysis_gdf))
    if functions_analysis.is_gdf(nn_analysis_gdf) is False:
        raise ValueError(valerror_text)
        
    attriberror_text = "Argument provided does not have geometry information."
    if functions_analysis.has_geometry(nn_analysis_gdf) is False:
        raise AttributeError(attriberror_text)
        
    attriberror_text = "nn_analysis_gdf object is missing crs information."
    if functions_analysis.has_crs(nn_analysis_gdf) is False:
        raise AttributeError(attriberror_text)
        
    fig = plt.figure(figsize = (10,10))
    ax_1 = fig.add_subplot(1,1,1)
    
    for spine in ax_1.spines:
        ax_1.spines[spine].set_visible(False)
    
    ax_1.xaxis.set_visible(False)
    ax_1.yaxis.set_visible(False)
        
    color_3 = "#1CB2FE"
    color_4 = "#F68C69"
    color_5 = "#1A1C1A"
    
    fig.set_facecolor(color_5)
    ax_1.set_facecolor(color_5)
    
    nn_analysis_gdf["links"] = link_gseries
    
    nn_analysis_gdf.set_geometry("links", inplace = True)
    nn_analysis_gdf.plot(ax = ax_1,
                        color = "white",
                        alpha = 1,
                        lw=1)
    
    nn_analysis_gdf.set_geometry("point_of_origin", inplace = True)
    nn_analysis_gdf["point_of_origin"].plot(ax = ax_1,
                                   color = color_3,
                                   alpha = 1,
                                   zorder = 2,
                                   markersize = 70,
                                   marker = "o",
                                   edgecolor = "white")
    
    nn_analysis_gdf.set_geometry("nearest_point", inplace = True)
    nn_analysis_gdf["nearest_point"].plot(ax = ax_1,
                                 color = color_4,
                                 zorder = 3,
                                 alpha = 1,
                                 markersize = 70,
                                 marker = "^",
                                 edgecolor = "white")
    
    plt.tight_layout()
    
    return fig
    
#%% --- Main Function ---
def confirm_nearest_neighbor_analysis(nn_analysis_gdf, save_figure = False):
    valerror_text = "Argument nn_analysis_gdf should be of type geopandas.GeoDataFrame. Got {} ".format(type(nn_analysis_gdf))
    if functions_analysis.is_gdf(nn_analysis_gdf) is False:
        raise ValueError(valerror_text)
        
    attriberror_text = "Argument provided does not have geometry information."
    if functions_analysis.has_geometry(nn_analysis_gdf) is False:
        raise AttributeError(attriberror_text)
    
    fig = plot_nearest_neighbor_analysis(nn_analysis_gdf,
                                   create_link_between_origin_and_nearest_geom(nn_analysis_gdf))
    
    if save_figure == True:
        fig.savefig("nearest_neighbor_analysis_confirmation.png",
            dpi = 1200,
            bbox_inches='tight',
            pad_inches = 0)
        
    return fig

#%% --- FUNCTION --- add_watermark ---
#%% --- Main function ---
def add_watermark(fig, watermark_str, ax_is_constrained = False,
                  position_x = 0.85, position_y = 0.09):
    """
    Watermarks the selected plot with a given selected string.
    The watermark is located at the lower right corner of the plot.

    Parameters
    ----------
    plt :matplotlib.Figure
    
    watermark_str : Python str object
    
    position_x : Python int or float
        
    position_y : Python int or float

    Returns
    -------
    None.

    """
    
    valerror_text = "Argument fig should be of type matplotlib.Figure. Got {} ".format(type(fig))
    if not isinstance(fig, plt.Figure):
        raise ValueError(valerror_text)
        
    valerror_text = "Argument watermark_str should be of type str. Got {} ".format(type(watermark_str))
    if not isinstance(watermark_str, str):
        raise ValueError(valerror_text)
    
    plt.gcf().text(position_x,
                   position_y,
                   watermark_str, 
                   alpha=0.5)
    
#%% --- FUNCTION: label_district_on_map --

def label_district_on_map(ax_object, geodataframe, column_to_look_at, districts_list):
    labels_mask = geodataframe.loc[:,column_to_look_at].isin(districts_list)
    districts_to_label = geodataframe.loc[labels_mask,[column_to_look_at, "geometry"]]
    districts_to_label["representative_point"] = districts_to_label.geometry.representative_point().geometry.values
    
    for idx, row in districts_to_label.iterrows():
        ax_object.annotate(s=row[column_to_look_at], xy=(row["representative_point"].x,row["representative_point"].y),
                 horizontalalignment='center')
        
#%% --- FUNCTION: create_cmap_in_figure ---

def create_cmap_legend_in_figure(ax,label, label_size, label_weight, cmap_object,
                                 legend_height = "5%", legend_width = "50%", legend_loc = "upper right",
                                 orientation = "horizontal", shrink = 0.25,
                                 anchor = (30,10)):

    
    from mpl_toolkits.axes_grid1.inset_locator import inset_axes
    
    #Create an inset axis within the main ax
    axins = inset_axes(ax,
                       height = legend_height,
                       width = legend_width,
                       loc = legend_loc)

    cbar = plt.colorbar(cmap_object,
                        cax = axins,
                        # ticks = [] Cna also set ticks like this
                        orientation = orientation,
                        shrink = shrink,
                        anchor = anchor)
    
    cbar.set_label(label,
                    size = label_size,
                    weight = label_weight)
    
    return (axins,cbar)

#%% --- FUNCTION: add_value_labels_on_bar_chart

def add_value_labels_bar(ax, spacing=5):
    """Add labels to the end of each bar in a bar chart.

    Arguments:
        ax (matplotlib.axes.Axes): The matplotlib object containing the axes
            of the plot to annotate.
        spacing (int): The distance between the labels and the bars.
    """

    # For each bar: Place a label
    for rect in ax.patches:
        # Get X and Y placement of label from rect.
        y_value = rect.get_height()
        x_value = rect.get_x() + rect.get_width() / 2

        # Number of points between bar and label. Change to your liking.
        space = spacing
        # Vertical alignment for positive values
        va = 'bottom'

        # If value of bar is negative: Place label below bar
        if y_value < 0:
            # Invert space to place label below
            space *= -1
            # Vertically align label at top
            va = 'top'

        # Use Y value as label and format number with one decimal place
        label = "{:}".format(y_value) #Remove .1f if you don't want one decimal place

        # Create annotation
        ax.annotate(
            label,                      # Use `label` as label
            (x_value, y_value),         # Place label at end of the bar
            xytext=(0, space),          # Vertically shift label by `space`
            textcoords="offset points", # Interpret `xytext` as offset in points
            ha='center',                # Horizontally center label
            va=va,                      # Vertically align label differently for  positive and negative values.
            rotation = 90,
            fontsize = 12)              # Rotate label
        
def add_value_labels_barh(ax, spacing=5, fontsize = 12):
    """Add labels to the end of each bar in a bar chart.

    Arguments:
        ax (matplotlib.axes.Axes): The matplotlib object containing the axes
            of the plot to annotate.
        spacing (int): The distance between the labels and the bars.
    """

    # For each bar: Place a label
    for rect in ax.patches:
        # Get X and Y placement of label from rect.
        x_value = rect.get_width()
        y_value = rect.get_y() + rect.get_height() / 2

        # Number of points between bar and label. Change to your liking.
        space = spacing * -1
        # Vertical alignment for positive values
        ha = 'right'

        # If value of bar is negative: Place label below bar
        if x_value < 0:
            # Invert space to place label below
            space = spacing
            # Vertically align label at top
            ha = 'left'

        # Use Y value as label and format number with one decimal place
        label = "{:}".format(x_value) #Remove .1f if you don't want one decimal place

        # Create annotation
        ax.annotate(
            label,                      # Use `label` as label
            (x_value, y_value),         # Place label at end of the bar
            xytext=(space, 0),          # Vertically shift label by `space`
            textcoords="offset points", # Interpret `xytext` as offset in points
            ha=ha,                # Horizontally center label
            va="center",                      # Vertically align label differently for  positive and negative values.
            rotation = 0,
            fontsize = fontsize)
                                 
    
