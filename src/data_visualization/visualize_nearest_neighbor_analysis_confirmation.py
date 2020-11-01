# -*- coding: utf-8 -*-
"""
------ What is this file? ------

This script targets one file:
    - istanbul_airbnb_processed.csv
    
The script produces histograms for the distribution of Airbnb
prices in the city of Istanbul. 

Returns five histograms that visualize Airbnb rental price distribution
under different slices.
"""
#%% --- Import Required Packages ---

import os
from pathlib import Path # To wrap around filepaths
from shapely.geometry import Point
import pandas as pd
import geopandas as gpd
from src.helper_functions.data_visualization_helper_functions import confirm_nearest_neighbor_analysis

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Import Data ---

#Istanbul districts
import_fp = Path("../../data/external/istanbul_districts.shp")
istanbul_districts = gpd.read_file(import_fp, encoding = "utf-8-sig")

#All districts - raw
import_fp = Path("../../data/final/nn_analysis_results_all.csv")
nn_analysis_results_all = pd.read_csv(import_fp, encoding = "utf-8-sig")

#All districts - normalized
import_fp = Path("../../data/final/nn_analysis_results_normalized.csv")
nn_analysis_results_normalized = pd.read_csv(import_fp, encoding = "utf-8-sig")

#Selected districts - normalized
districts = ["atasehir", "besiktas", "kadikoy", "sisli", "uskudar"]

nn_analysis_results_per_district = {}

for district in districts:
    import_fp = Path("../../data/final/nn_analysis_results_norm_{}.csv".format(district))
    nn_analysis_results_per_district[district] = pd.read_csv(import_fp, encoding = "utf-8-sig")
    

#%% --- De-code and Re-code geometry information ---

#Create a function to transform strings into tuples
def decode_recode_point_str(point_str):
    split = point_str.split()
    lon = float(split[1].strip("("))
    lat = float(split[2].strip(")"))
    return Point(lon,lat)

#Apply functions to dataframes
#Raw
nn_analysis_results_all.loc[:,"point_of_origin"] = nn_analysis_results_all.loc[:,"point_of_origin"].apply(decode_recode_point_str)
nn_analysis_results_all.loc[:,"nearest_point"] = nn_analysis_results_all.loc[:,"nearest_point"].apply(decode_recode_point_str)

#Normalized
nn_analysis_results_normalized.loc[:,"point_of_origin"] = nn_analysis_results_normalized.loc[:,"point_of_origin"].apply(decode_recode_point_str)
nn_analysis_results_normalized.loc[:,"nearest_point"] = nn_analysis_results_normalized.loc[:,"nearest_point"].apply(decode_recode_point_str)

#Selected districts
for dataframe in nn_analysis_results_per_district.values():
    dataframe.loc[:,"point_of_origin"] = dataframe.loc[:,"point_of_origin"].apply(decode_recode_point_str)
    dataframe.loc[:,"nearest_point"] = dataframe.loc[:,"nearest_point"].apply(decode_recode_point_str)
    
#%% --- Turn dataframes to geodataframes ---

#Set a reference crs
reference_crs = istanbul_districts.crs

#Turn dataframes into datasets
#Raw
nn_analysis_results_all_gdf = gpd.GeoDataFrame(nn_analysis_results_all,
                                               crs = reference_crs,
                                               geometry = "point_of_origin")

#Normalized
nn_analysis_results_normalized_gdf = gpd.GeoDataFrame(nn_analysis_results_normalized,
                                                      crs = reference_crs,
                                                      geometry = "point_of_origin")
#Selected districts
nn_analysis_results_per_district_gdf = {}

for district_name, district_df in nn_analysis_results_per_district.items():
    nn_analysis_results_per_district_gdf[district_name] = gpd.GeoDataFrame(district_df,
                                                                           crs = reference_crs,
                                                                           geometry = "point_of_origin")
    




