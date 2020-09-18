# -*- coding: utf-8 -*-
"""
------ What is this file? ------

This script contains some helper functions that are used in the scripts
found under src/data_visualization.


"""

#%% --- Import required packages ---

import os
import matplotlib.pyplot as plt
from src.helper_functions import data_analysis_helper_functions as functions_analysis

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
