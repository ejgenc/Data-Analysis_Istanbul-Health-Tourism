# -*- coding: utf-8 -*-
"""
------ What is this file? ------

This script targets two files:
    - nn_analysis_results_all.csv
    - istanbul_airbnb_processed_shapefile.shp
    
This script prepares and merges the two files for further analysis.
Every row is an Airbnb rental. For each Airbnb rental,
the following information is retained:
    - district in which the rental can be found
    - rental price
    - exact location (geometry)
    - nearest health tourism-related institution (nearest_point)
    - distance between the Airbnb rental and the nearest
        health-tourism related institution.
        
Returns a single shapefile.

"""
#%% --- Import Required Packages ---

import os
from pathlib import Path # To wrap around filepaths
from shapely.geometry import Point
import pandas as pd
import geopandas as gpd

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Import Data ---

#Nearest neighbor analysis results
import_fp = Path("../../data/final/nn_analysis_results_all.csv")
nn_results = pd.read_csv(import_fp, encoding = "utf-8-sig")

#Airbnb data in geospatial form
import_fp = Path("../../data/processed/istanbul_airbnb_processed_shapefile.shp")
airbnb = gpd.read_file(import_fp, encoding = "utf-8-sig")

#%% --- Drop irrelevant Airbnb columns ---

#Keep only the colums that will be needed in masking/viz./analysis
columns_to_keep = ["district_e", "price", "geometry"]
airbnb =  airbnb.loc[:,columns_to_keep]

#%% --- Turn nn_results into a GeoDataFrame ---

#Create a function to transform strings into tuples
def decode_recode_point_str(point_str):
    split = point_str.split()
    lon = float(split[1].strip("("))
    lat = float(split[2].strip(")"))
    return Point(lon,lat)

# Decode and recode point info, goes from str to shapely Point object.
nn_results.loc[:,"point_of_origin"] = (nn_results.loc[:,"point_of_origin"]
                                       .apply(decode_recode_point_str))

#Create a GeoDataFrame with the same crs as airbnb dataset
nn_results_gdf = gpd.GeoDataFrame(nn_results,
                                  crs = airbnb.crs,
                                  geometry = "point_of_origin")

#%% --- Merge two GeoDataFrames ---

#Do a left spatial join on airbnb
distance_price_dataset = gpd.sjoin(airbnb,
                                   nn_results_gdf,
                                   how = "left",
                                   op = "intersects")

distance_price_dataset.drop("index_right", axis = 1, inplace = True)

#%% --- Export data ---

out_fp = Path("../../data/final/distance_price_dataset.shp")
distance_price_dataset.to_file(out_fp)