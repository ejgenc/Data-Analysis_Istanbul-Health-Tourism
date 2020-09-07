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
    valerror_text = ("Both function arguments should be of type geopandas.GeoDataFrame"
    "Got {} and {}").format(type(reference_geodataframe), type(comparison_geodataframe))
    if not isinstance(reference_geodataframe, gpd.geodataframe.GeoDataFrame) or not isinstance(comparison_geodataframe, gpd.geodataframe.GeoDataFrame):
        raise ValueError(valerror_text)
        
    valerror_text = "At least one geopandas.GeoDataFrame object is missing crs information."
    if reference_geodataframe.crs is None or comparison_geodataframe.crs is None:
        raise ValueError(valerror_text)
    
    return reference_geodataframe.crs == comparison_geodataframe.crs

def has_geometry():
    pass

#%%     --- Subfunctions ---

def calculate_centroid(geodataframe):
    pass

def create_unary_union(geodataframe):
    pass

def calculate_nearest_neighbor():
    pass

def calculate_distance():
    pass

#%%     --- Main Function ---


def nearest_neighbor_analysis(gdf1, gdf2):
    '''
Accepts as an an argument two Geopandas GeoDataFrames
Takes the gdf1 as the GeoDataFrame of origin and gdf2 as the GeoDataFrame of query
For each element of gdf1, finds which element of gdf2 is closest and also calculates the distance
Returns a GeoDataFrame containing origin geometry, nearest geometry and the distance in meters

NOTE: gdf2 is turned into a MultiPoint object first through unary union.
NOTE: This method is extremely slow as it is not vectorized. Proceed with caution.
Note: The distance is calculated via geopy 
    '''
    
#Calculate the centroid of gdf2

    gdf2_copy = gdf2.copy()

    gdf2_copy["centroid"] = gdf2_copy.geometry.centroid

#Set geometry of gdf2_copy
    gdf2_copy.set_geometry("centroid", inplace = True)
    
#Take the unary union of gdf2_copy
    gdf2_copy_bundled = gdf2_copy.geometry.unary_union
    
#Create an empty list of series to store individual series
    lst_of_series = []
    
#Iterate over gdf1
        
    for index, row in gdf1.iterrows():
        
        #For each row, do the actual nearest points analysis
        points = nearest_points(row["geometry"], gdf2_copy_bundled)
        
        #Create a mask for the gdf2_copy
        mask = gdf2_copy.geometry == points[1]
        
        #Select data based on that mask
        
        data = gdf2_copy.loc[mask,["centroid"]]
        
        #Create a backlink to the point from which the query is made
        
        data["origin_geometry"] = row["geometry"]
        
        #Do the distance calculation
        
        origin_geom_coords = data["origin_geometry"].values[0].coords
        query_centroid_coords = data["centroid"].values[0].coords
        
        data["distance_origin_to_centroid"] = distance.distance(origin_geom_coords,
                                                                query_centroid_coords).m
        
        lst_of_series.append(data)
    
#Now we can turn turn the lst_of_series into a geodataframe
    
    gdf_final = gpd.GeoDataFrame(pd.concat(lst_of_series, ignore_index = True),
                                 crs = lst_of_series[0].crs)
    
    return gdf_final
