# -*- coding: utf-8 -*-
"""
------ What is this file? ------

This script targets two files:
    - istanbul_airbnb_processed_shapefile.shp
    - htourism_centers_processed.shp
The script combines conducts a nearest neighbor analysis by taking 
istanbul_airbnb_processed as reference and htourism_centers_processed as comparison.

Returns a dataframe that includes information about the nearest health tourism center
to each AirBnB rental along with the distance.
"""
#%% --- Import Required Packages ---

import os
from pathlib import Path # To wrap around filepaths
import numpy as np
import pandas as pd
import geopandas as gpd
from src.helper_functions.data_analysis_helper_functions import nearest_neighbor_analysis,confirm_nearest_neighbor_analysis 
#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Import Data ---

#Import airbnb data
import_fp = Path("../../data/processed/istanbul_airbnb_processed_shapefile.shp")
airbnb_gdf = gpd.read_file(import_fp, encoding = "utf-8-sig")

#Import htourism centers data
import_fp = Path("../../data/processed/htourism_centers_processed.shp")
htourism_gdf = gpd.read_file(import_fp, encoding = "utf-8-sig")

#Import Istanbul districts data
import_fp = Path("../../data/external/istanbul_districts.shp")
istanbul_districts = gpd.read_file(import_fp, encoding = "utf-8-sig")

#%% --- Conduct Nearest Neighbor Analysis for all districts ---

nn_analysis_results_all = nearest_neighbor_analysis(airbnb_gdf, htourism_gdf)

#%% --- Conduct Nearest Neighbor Analysis for five districts with most Htourism centers ---

nn_analysis_results_districts = {}
selected_districts = ["Sisli", "Besiktas", "Kadikoy", "Atasehir", "Uskudar"]

for district in selected_districts:
    district_mask = airbnb_gdf.loc[:,"district_e"] == district
    selection = airbnb_gdf.loc[district_mask,:]
    result = nearest_neighbor_analysis(selection, htourism_gdf)
    nn_analysis_results_districts[district] = result
    
#%% --- Plot 'em ---
# for district in nn_analysis_results_districts.keys():
#     confirm_nearest_neighbor_analysis(nn_analysis_results_districts[district])

#%% --- Export data : nn_analysis_results_all ---

export_fp = Path("../../data/final/nn_analysis_results_all.csv")
nn_analysis_results_all.to_csv(export_fp, encoding = "utf-8-sig")

#%% --- Export data: nn_analysis_results_districts ---

for district, nn_analysis in nn_analysis_results_districts.items():
    path_string = ("../../data/final/nn_analysis_results_{}.csv").format(district)
    export_fp = Path(path_string)
    nn_analysis.to_csv(export_fp, encoding = "utf-8-sig")






