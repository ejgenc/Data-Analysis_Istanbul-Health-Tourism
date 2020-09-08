# -*- coding: utf-8 -*-
"""
------ What is this file? ------

This script contains some helper functions that are used in the scripts foundunder src/data_analysis.
The unit tests for these functions can be found at:
     tests/unit_tests/helper_functions/test_data_preparation_helper_functions.py

"""

#%% --- Import Required Packages ---

import os
from pathlib import Path # To wrap around filepaths
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, MultiPoint
from shapely.ops import nearest_points
from geopy import distance


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
        
    attriberror_text= "Argument provided does not have geometry information."
    if has_geometry(geodataframe) is False:
        raise AttributeError(attriberror_text)
        
    if isinstance(geodataframe.geometry[0], Point):
        centroids = geodataframe.geometry
    else:
        centroids = geodataframe.geometry.centroid
        
    return centroids

def create_unary_union(geodataframe):
    ### Accepts a geodataframe
    ### Geodataframe has geometry information
    ### Geometry information is composed of points
    ### Creates a unary union
    ### Returns the unary union
    pass

def calculate_nearest_neighbor():
    pass

def calculate_distance():
    pass

#%%     --- Main Function ---

def nearest_neighbor_analysis(reference_geodataframe, comparison_geodataframe):
    
    gdf_list = [reference]
    
    valerror_text = ("Both arguments should be geopandas.GeoDataFrame objects."
                     "Got {} and {} as object types.").format(type(reference_geodataframe), type(comparison_geodataframe))
    if check_if_all_elements_are_gdf(gdf_list) is False:
        raise ValueError(valerror_text)
    
    attriberror_text= ("At least one of the arguments provided do not have geometry information.")
    if check_if_all_elements_have_geometry(gdf_list) is False:
        raise AttributeError(attriberror_text)
 
    attriberror_text = ("The arguments provided to do not share the same crs."
                        "Got {} and {} as crs.").format(reference_geodataframe.crs, comparison_geodataframe.crs)
    if crs_is_equal(reference_geodataframe, comparison_geodataframe) is False:
        raise AttributeError(attriberror_text)
        
    # FUNCTION: PREPARE FOR NN #
        # - Get centroids
        # - Create unary union of centroids
    
    # FUNCTION: NN Analysis
    
    # If calculate_distance is True:
    # FUNCTION: Do the distance calculations
        # Check for parameters
        
    # Return final gdf


#%%
# def nearest_neighbor_analysis(gdf1, gdf2):
#     '''
# Accepts as an an argument two Geopandas GeoDataFrames
# Takes the gdf1 as the GeoDataFrame of origin and gdf2 as the GeoDataFrame of query
# For each element of gdf1, finds which element of gdf2 is closest and also calculates the distance
# Returns a GeoDataFrame containing origin geometry, nearest geometry and the distance in meters

# NOTE: gdf2 is turned into a MultiPoint object first through unary union.
# NOTE: This method is extremely slow as it is not vectorized. Proceed with caution.
# Note: The distance is calculated via geopy 
#     '''
    
# #Calculate the centroid of gdf2

#     gdf2_copy = gdf2.copy()

#     gdf2_copy["centroid"] = gdf2_copy.geometry.centroid

# #Set geometry of gdf2_copy
#     gdf2_copy.set_geometry("centroid", inplace = True)
    
# #Take the unary union of gdf2_copy
#     gdf2_copy_bundled = gdf2_copy.geometry.unary_union
    
# #Create an empty list of series to store individual series
#     lst_of_series = []
    
# #Iterate over gdf1
        
#     for index, row in gdf1.iterrows():
        
#         #For each row, do the actual nearest points analysis
#         points = nearest_points(row["geometry"], gdf2_copy_bundled)
        
#         #Create a mask for the gdf2_copy
#         mask = gdf2_copy.geometry == points[1]
        
#         #Select data based on that mask
        
#         data = gdf2_copy.loc[mask,["centroid"]]
        
#         #Create a backlink to the point from which the query is made
        
#         data["origin_geometry"] = row["geometry"]
        
#         #Do the distance calculation
        
#         origin_geom_coords = data["origin_geometry"].values[0].coords
#         query_centroid_coords = data["centroid"].values[0].coords
        
#         data["distance_origin_to_centroid"] = distance.distance(origin_geom_coords,
#                                                                 query_centroid_coords).m
        
#         lst_of_series.append(data)
    
# #Now we can turn turn the lst_of_series into a geodataframe
    
#     gdf_final = gpd.GeoDataFrame(pd.concat(lst_of_series, ignore_index = True),
#                                  crs = lst_of_series[0].crs)
    
#     return gdf_final


