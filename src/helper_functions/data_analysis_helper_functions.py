# -*- coding: utf-8 -*-
"""
------ What is this file? ------

This script contains some helper functions that are used in the scripts found under src/data_analysis.
The unit tests for these functions can be found at:
     tests/unit_tests/helper_functions/test_data_preparation_helper_functions.py

"""
#%% --- Import Required Packages ---

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, MultiPoint, LineString
from shapely.ops import nearest_points
from geopy import distance
import matplotlib.pyplot as plt
 
#%% --- FUNCTION : nearest_neighbor_analysis ---

#%%     --- Helper Functions ---

def is_gdf(argument):
    """
    Check the given argument to see if it is of type geopandas.GeoDataFrame
    
    Parameters
    ----------
    argument : A single argument of any type

    Returns
    -------
    bool
        True if argument is of type geopandas GeoDataFrame.
        False if argument is not of type geopandas GeoDataFrame

    """
    if not isinstance(argument, gpd.geodataframe.GeoDataFrame):
        return False
        
    return True

def check_if_all_elements_are_gdf(arguments_list):
    """
    Checks if the elements of a list are instances of geopandas.GeoDataFrame
    
    Parameters
    ----------
    arguments_list : A single argument of type list
        The list contains all elements that will be typechecked by is_gdf()

    Returns
    -------
    bool
        True if all elements of arguments_list is an instance of gpd.GeoDataFrame
        False if at least one elemnt is not an instance of gpd.GeoDataFrame
    """
    valerror_text = "arguments_list must be of type list. Got {}".format(type(arguments_list))
    if not isinstance(arguments_list, list):
        raise ValueError(valerror_text)
    
    for argument in arguments_list:
        if is_gdf(argument) is False:
            return False
        
    return True
    
def has_crs(geodataframe):
    """
    Checks if the given geopandas GeoDataFrame has crs information.

    Parameters
    ----------
    geodataframe: A geopandas.GeoDataFrame object.

    Returns
    -------
    True if geodataframe has crs information specified.
    False if geodataframe doesn't have crs information specified.

    """
    valerror_text = "Function argument should be of type geopandas.GeoDataFrame. Got {}".format(type(geodataframe))
    if is_gdf(geodataframe) is False:
        raise ValueError(valerror_text)
        
    if geodataframe.crs is None:
        return False
        
    return True
        
def check_if_all_elements_have_crs(geodataframes_list):
    """
    Iterates over a list and checks if all members of the list have crs
    information associated with them.

    Parameters
    ----------
    geodataframes_list : A list object
        A list object that contains one or more geopandas.GeoDataFrame objects

    Returns
    -------
    bool
        Returns True if all elements within geodataframes_list have crs info associated with them
        Returns False if atleast one element within geodataframes_list does not have crs info associated with it

    """
    
    valerror_text = "geodataframes_list must be of list type. Got {}".format(type(geodataframes_list))
    if not isinstance(geodataframes_list, list):
        raise ValueError(valerror_text)
    
    valerror_text = "Elements of the list should be of type geopandas.GeoDataFrame. Got at least one value that is not."
    if check_if_all_elements_are_gdf(geodataframes_list) is False:
        raise ValueError(valerror_text)
            
    for geodataframe in geodataframes_list:
        if has_crs(geodataframe) is False:
            return False
        
    return True
        

def has_geometry(geodataframe):
    """
    Checks if the given geopandas.GeoDataFrame object has geometry information.

    Parameters
    ----------
    geodataframe: A geopandas.GeoDataFrame object.

    Returns
    -------
    True if geodataframe has geometry information specified.
    False if geodataframe doesn't have geometry information specified.

    """
    
    valerror_text = "Function argument should be of type geopandas.GeoDataFrame. Got {} ".format(type(geodataframe))
    if is_gdf(geodataframe) is False:
        raise ValueError(valerror_text)
    
    try:
        geodataframe.geometry  
    except AttributeError:
        return False
    
    return True
        
def check_if_all_elements_have_geometry(geodataframes_list):
    """
    Iterates over a list and checks if all members of the list have geometry
    information associated with them.

    Parameters
    ----------
    geodataframes_list : A list object
        A list object that contains one or more geopandas.GeoDataFrame objects

    Returns
    -------
    bool
        Returns True if all elements within geodataframes_list have geometry info associated with them
        Returns False if atleast one element within geodataframes_list does not have geometry info associated with it

    """
    
    valerror_text = "geodataframes_list must be of list type. Got {}".format(type(geodataframes_list))
    if not isinstance(geodataframes_list, list):
        raise ValueError(valerror_text)
        
    valerror_text = "Elements of the list should be of type geopandas.GeoDataFrame. Got at least one value that is not."
    if check_if_all_elements_are_gdf(geodataframes_list) is False:
        raise ValueError(valerror_text)
    
    for geodataframe in geodataframes_list:
        if has_geometry(geodataframe) is False:
            return False

    return True

def crs_is_equal(reference_geodataframe, comparison_geodataframe):
    """
    Checks if two geopandas GeoDataFrame objects share the same crs.

    Parameters
    ----------
    reference_geodataframe : geopandas GeoDataFrame object.
    comparison_geodataframe : geopandas GeoDataFrame object.

    Returns
    -------
    True if both GeoDataFrame objects share the same crs.

    """        
    #The values we recieve are turned into gdf to make use of
    #the list checking functions i've built
    gdf_list = [reference_geodataframe, comparison_geodataframe]
    
    # Check if gdf_list is gdf
    valerror_text = "Both function arguments should be of type geopandas.GeoDataFrame"
    if check_if_all_elements_are_gdf(gdf_list) is False:
        raise ValueError(valerror_text)
        
    # Check if gdf_list has crs info
    attriberror_text = "At least one geopandas.GeoDataFrame object is missing crs information."
    if check_if_all_elements_have_crs(gdf_list) is False:
        raise AttributeError(attriberror_text)
    
    return reference_geodataframe.crs == comparison_geodataframe.crs

def map_geometry_types(geodataframe, return_most_common = False):
    """
    Calculates a value - count table for each type of geometry object
    that appears in the geometry column of the targeted geodataframe.

    Parameters
    ----------
    geodataframe : geopandas GeoDataFrame object.

    return_most_common : Boolean, optional
        Affects what is returned.
        If True, function returns a tuple.
        If False, function returns a pd.Series

    Returns
    -------
    Tuple if return_most_common == True
        Returns a tuple that contains the most recurring geometry type and how many times it appears
        
    pandas.Series if return_most_commo == False
        A series that shows how many time each geometry type appears.

    """
    valerror_text = "Argument provided should be of type geopandas.GeoDataFrame. Got {} ".format(type(geodataframe))
    if is_gdf(geodataframe) is False:
        raise ValueError(valerror_text)
        
    attriberror_text = "Argument provided does not have geometry information."
    if has_geometry(geodataframe) is False:
        raise AttributeError(attriberror_text)
        
    valerror_text = "Only Boolean True/False can be passed as an argument to return_most_common"
    if not isinstance(return_most_common, bool):
        raise ValueError(valerror_text)
    
    geometry_types = geodataframe.geometry.geom_type
    
    value_counts = geometry_types.value_counts()
    
    if return_most_common == True:
        most_common_value_pair = (value_counts.index[0], value_counts[0])
        return most_common_value_pair
    
    return value_counts
    
#%%     --- Subfunctions ---

def calculate_centroid(geodataframe):
    """
    Calculates the centroid of each geometry datapoint in the geodataframe.

    Parameters
    ----------
    geodataframe : geopandas GeoDataFrame object.

    Returns
    -------
    centroids : geopandas.GeoSeries object.
        A geopandas.GeoSeries object that has the information about the centroid of
        each geometry datapoint in the original geodataframe

    """
    valerror_text = "Argument provided should be of type geopandas.GeoDataFrame. Got {} ".format(type(geodataframe))
    if is_gdf(geodataframe) is False:
        raise ValueError(valerror_text)
        
    attriberror_text = "Argument provided does not have geometry information."
    if has_geometry(geodataframe) is False:
        raise AttributeError(attriberror_text)
        
    if isinstance(geodataframe.geometry[0], Point):
        centroids = geodataframe.geometry
    else:
        centroids = geodataframe.geometry.centroid
        
    return gpd.GeoDataFrame(centroids,
                            crs = geodataframe.crs)

def create_unary_union(geodataframe):
    """
    Creates a unary union from the geometry datapoints of the given
    geopandas GeoDataFrame object.

    Parameters
    ----------
    geodataframe : geopandas GeoDataFrame object.

    Returns
    -------
    unary_union : shapely.geometry.multipoint.MultiPoint object
        A shapely MultiPoint object that is composed from the geometry datapoints
        of the given geopandas GeoDataFrame object.

    """
    valerror_text = "Argument provided should be of type geopandas.GeoDataFrame. Got {} ".format(type(geodataframe))
    if is_gdf(geodataframe) is False:
        raise ValueError(valerror_text)
        
    attriberror_text = "Argument provided does not have geometry information."
    if has_geometry(geodataframe) is False:
        raise AttributeError(attriberror_text)
        
    attriberror_text = ("Geometry information of the argument provided should be composed of Points."
                        "Found at least one non-point shape.")
    most_common_geom = map_geometry_types(geodataframe, return_most_common = True)
    if most_common_geom[0] != "Point":
        raise AttributeError(attriberror_text)
    
    unary_union = geodataframe.geometry.unary_union
    
    return unary_union

def prepare_for_nearest_neighbor_analysis(geodataframe):
    """
    Calculates the centroid of all geometry datapoints of the given dataframe
    by calling calculate_centroid.
    After calculating the centroids, composes a unary union of all the centroids.

    Parameters
    ----------
    geodataframe : geopandas GeoDataFrame object.

    Returns
    -------
    geodataframe_prepared :  shapely.geometry.multipoint.MultiPoint object
        A shapely MultiPoint object that is composed from the centroids
        of the given geopandas GeoDataFrame object.

    """
    valerror_text = "Argument provided should be of type geopandas.GeoDataFrame. Got {} ".format(type(geodataframe))
    if is_gdf(geodataframe) is False:
        raise ValueError(valerror_text)
        
    attriberror_text = "Argument provided does not have geometry information."
    if has_geometry(geodataframe) is False:
        raise AttributeError(attriberror_text)
        
    attriberror_text = ("Geometry information of the argument provided should be composed of Points."
                        "Found at least one non-point shape.")
    most_common_geom = map_geometry_types(geodataframe, return_most_common = True)
    if most_common_geom[0] != "Point":
        raise AttributeError(attriberror_text)
    
    geodataframe_prepared = create_unary_union(calculate_centroid(geodataframe))
    return geodataframe_prepared

def calculate_nearest_neighbor(geodataframe, multipoint_obj):
    valerror_text = "Argument geodataframe should be of type geopandas.GeoDataFrame. Got {} ".format(type(geodataframe))
    if is_gdf(geodataframe) is False:
        raise ValueError(valerror_text)
        
    attriberror_text = "Argument provided does not have geometry information."
    if has_geometry(geodataframe) is False:
        raise AttributeError(attriberror_text)
        
    attriberror_text = ("Geometry information of the argument provided should be composed of Points."
                        "Found at least one non-point shape.")
    most_common_geom = map_geometry_types(geodataframe, return_most_common = True)
    if most_common_geom[0] != "Point":
        raise AttributeError(attriberror_text)
        
    valerror_text = "Argument multipoint_obj should be of type shapely.geometry.MultiPoint. Got {} ".format(type(multipoint_obj))
    if not isinstance(multipoint_obj, MultiPoint):
        raise ValueError(valerror_text)
    
    nearest_points_list = []
    for index, row in geodataframe.iterrows():
        point_of_origin = row.geometry
        nearest_points_tuple = nearest_points(point_of_origin, multipoint_obj)
        nearest_point = nearest_points_tuple[1]
        nearest_points_list.append([point_of_origin, nearest_point])
        
        
    nearest_points_gdf = gpd.GeoDataFrame(nearest_points_list,
                                          columns = ["point_of_origin",
                                                     "nearest_point"],
                                          crs = geodataframe.crs,
                                          geometry = "point_of_origin")

    return nearest_points_gdf
    
def calculate_distance(nearest_points_gdf):
    valerror_text = "Argument nearest_points_gdf should be of type geopandas.GeoDataFrame. Got {} ".format(type(nearest_points_gdf))
    if is_gdf(nearest_points_gdf) is False:
        raise ValueError(valerror_text)
        
    valerror_text = "The geodataframe provided does not contain columns point_of_origin and nearest_point"
    if not ("point_of_origin" in nearest_points_gdf.columns and "nearest_point" in nearest_points_gdf.columns):
        raise ValueError(valerror_text)
        
    distances = [distance.distance(p1.coords,p2.coords).m for p1,p2 in nearest_points_gdf.loc[:,["point_of_origin","nearest_point"]].values]
    
    return pd.Series(distances)

#%%     --- Main Function ---

def nearest_neighbor_analysis(reference_geodataframe, comparison_geodataframe, distance = True):
        
    valerror_text = ("Both arguments should be geopandas.GeoDataFrame objects."
                     "Got {} and {} as object types.").format(type(reference_geodataframe), type(comparison_geodataframe))
    if check_if_all_elements_are_gdf([reference_geodataframe, comparison_geodataframe]) is False:
        raise ValueError(valerror_text)
    
    attriberror_text= ("At least one of the arguments provided do not have geometry information.")
    if check_if_all_elements_have_geometry([reference_geodataframe, comparison_geodataframe]) is False:
        raise AttributeError(attriberror_text)
 
    attriberror_text = ("The arguments provided to do not share the same crs."
                        "Got {} and {} as crs.").format(reference_geodataframe.crs, comparison_geodataframe.crs)
    if crs_is_equal(reference_geodataframe, comparison_geodataframe) is False:
        raise AttributeError(attriberror_text)
        
    comparison_geodataframe = prepare_for_nearest_neighbor_analysis(comparison_geodataframe)
    
    result = calculate_nearest_neighbor(reference_geodataframe, comparison_geodataframe)
    
    if distance == True:
        distances = calculate_distance(result)
        result["distance_in_meter"] = distances
    
    return result

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
