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
from scipy.stats import iqr
import geopandas as gpd
from src.helper_functions.data_analysis_helper_functions import nearest_neighbor_analysis
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
#%% --- Conduct Nearest Neighbor Analysis for all districts - without normalization ---

nn_analysis_results_all = nearest_neighbor_analysis(airbnb_gdf, htourism_gdf)

#%% --- Conduct Nearest Neighbor Analysis for all districts - with normalization ---

#Calculate iqr, q1 and q3 for price
price_iqr = iqr(airbnb_gdf.loc[:,"price"], axis = 0)
q1 = airbnb_gdf.loc[:,"price"].quantile(0.25)
q3 = airbnb_gdf.loc[:,"price"].quantile(0.75)

#Create masks to select values within IQR
min_mask = airbnb_gdf.loc[:,"price"] >= q1 - (price_iqr * 1.5)
max_mask = airbnb_gdf.loc[:,"price"] <= q3 + (price_iqr * 1.5)
combined_mask = min_mask & max_mask

#Select values according to mask 
airbnb_gdf_normalized = airbnb_gdf[combined_mask]

#Conduct nn analysis
nn_analysis_results_normalized = nearest_neighbor_analysis(airbnb_gdf_normalized,
                                                           htourism_gdf)

#%% --- Conduct Nearest Neighbor Analysis for five districts with most Htourism centers ---

nn_analysis_results_districts = {}
selected_districts = ["Sisli", "Besiktas", "Kadikoy", "Atasehir", "Uskudar"]

for district in selected_districts:
    district_mask = airbnb_gdf_normalized.loc[:,"district_e"] == district
    selection = airbnb_gdf_normalized.loc[district_mask,:]
    result = nearest_neighbor_analysis(selection, htourism_gdf)
    nn_analysis_results_districts[district] = result
    
#%% --- Export data : nn_analysis_results_all ---

export_fp = Path("../../data/final/nn_analysis_results_all.csv")
nn_analysis_results_all.to_csv(export_fp, encoding = "utf-8-sig")

#%% --- Export data : nn_analysis_results_normalized ---

export_fp = Path("../../data/final/nn_analysis_results_normalized.csv")
nn_analysis_results_normalized.to_csv(export_fp, encoding = "utf-8-sig")

#%% --- Export data: nn_analysis_results_districts ---

for district, nn_analysis in nn_analysis_results_districts.items():
    path_string = ("../../data/final/nn_analysis_results_norm_{}.csv").format(district.lower())
    export_fp = Path(path_string)
    nn_analysis.to_csv(export_fp, encoding = "utf-8-sig")






