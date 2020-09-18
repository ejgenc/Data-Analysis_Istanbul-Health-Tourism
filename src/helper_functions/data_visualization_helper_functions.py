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
    
#%% --- FUNCTION: setup_export_path ---
#%%
#Get the absolute filepath
dirname = os.path.dirname(__file__)

#Split by \ to make it into relative
dirname_intermediary = dirname.split("\\")

#Join in a way that would make it relative
separator = r"/"
dirname_final = separator.join(dirname_intermediary[0:5])

#Craft a filepath without the final folder to which the plot will be exported
incomplete_output_directory = dirname_final + "/Data Analysis_Istanbul Health Services Map/Media/Plots/"

#Get the name of the script
filename = os.path.basename(__file__)

#Split by _
filename_split = filename.split("_")

#Get the last to get the last folder name
filename_final = filename_split[-1]

#Remove the .py suffix
filename_final_processed = filename_final.split(".")[0]

#Craft the complete output directory
complete_output_directory = incomplete_output_directory + filename_final_processed

#Create the directory using os.mkdir.
try:
    os.mkdir(complete_output_directory)
except:
    pass

export_path = complete_output_directory +  r"/" + (filename_final_processed + "_eng.png")

def create_output_directory():
    #Get the absolute filepath
    dirname = os.path.dirname(__file__)

    #Split by \ to make it into relative
    dirname_intermediary = dirname.split("\\")
    
    #Find folder named src
    

#%%
def create_filename():
    #Get the name of the script
    filename = os.path.basename(__file__)

    #Split by _
    filename_split = filename.split("_")
    
    #Get the last to get the last folder name
    filename_final = filename_split[-1]

def setup_export_path():
    pass