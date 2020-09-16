# -*- coding: utf-8 -*-
"""
------ What is this file? ------

This script contains some helper functions that are used in the scripts
found under src/data_visualization.


"""

#%% --- Import required packages ---

import matplotlib.pyplot as plt

#%% --- FUNCTION : confirm_nearest_neighbor_analysis ---

#%% --- Subfunctions ---
def create_link_between_origin_and_nearest_geom(nn_analysis_gdf):
    valerror_text = "Argument nn_analysis_gdf should be of type geopandas.GeoDataFrame. Got {} ".format(type(nn_analysis_gdf))
    if is_gdf(nn_analysis_gdf) is False:
        raise ValueError(valerror_text)
        
    attriberror_text = "Argument provided does not have geometry information."
    if has_geometry(nn_analysis_gdf) is False:
        raise AttributeError(attriberror_text)
        
    attriberror_text = "nn_analysis_gdf object is missing crs information."
    if has_crs(nn_analysis_gdf) is False:
        raise AttributeError(attriberror_text)
        
    links = [LineString([p1,p2]) for p1, p2 in nn_analysis_gdf.loc[:,["point_of_origin","nearest_point"]].values]

    links_gseries = gpd.GeoSeries(links,
                              crs = nn_analysis_gdf.crs)
    
    return links_gseries

def plot_nearest_neighbor_analysis(nn_analysis_gdf, link_gseries):
    valerror_text = "Argument nn_analysis_gdf should be of type geopandas.GeoDataFrame. Got {} ".format(type(nn_analysis_gdf))
    if is_gdf(nn_analysis_gdf) is False:
        raise ValueError(valerror_text)
        
    attriberror_text = "Argument provided does not have geometry information."
    if has_geometry(nn_analysis_gdf) is False:
        raise AttributeError(attriberror_text)
        
    attriberror_text = "nn_analysis_gdf object is missing crs information."
    if has_crs(nn_analysis_gdf) is False:
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
    if is_gdf(nn_analysis_gdf) is False:
        raise ValueError(valerror_text)
        
    attriberror_text = "Argument provided does not have geometry information."
    if has_geometry(nn_analysis_gdf) is False:
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

#USE WITH BBOX INCHES
def add_watermark(ax):
    ax.text(ax.get_xlim()[1] - 1.5, 
            ax.get_ylim()[0] - 0.5,  
            "<Company Name>", 
            alpha=0.5)
    

def add_watermark_2(plt):
    plt.gcf().text(0.8,
                   0.09,
                   "<Company Name>", 
                   alpha=0.5)