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

#%% --- Conduct Nearest Neighbor Analysis ---

nn_analysis_results = nearest_neighbor_analysis(airbnb_gdf, htourism_gdf)

#%% --- Confirm Nearest Neighbor Analysis ---

nn_analysis_confirmation_plot = confirm_nearest_neighbor_analysis(nn_analysis_results)
#Although it seems as if it worked at first glance, it's better to 

#%% --- Re-do Nearest Neighbor Analysis confirmation on the scale of a single district ---

#Single out Sisli as a district
sisli_mask = istanbul_districts.loc[:,"district_e"] == "Sariyer"
sisli_only = istanbul_districts.loc[sisli_mask, :]

#Check which geometries in nn_analysis_results are in sisli
in_sisli_mask = nn_analysis_results.within(sisli_only.geometry.values[0])
in_sisli = nn_analysis_results.loc[in_sisli_mask, :]

nn_analysis_confirmation_plot = confirm_nearest_neighbor_analysis(in_sisli)


#%%

bsk_mask = airbnb_gdf.loc[:,"district_e"] == "Sariyer"
bsk_only = airbnb_gdf.loc[bsk_mask,:]

nn_analysis_results_2 = nearest_neighbor_analysis(bsk_only, htourism_gdf)
nn_analysis_confirmation_plot_2 = confirm_nearest_neighbor_analysis(nn_analysis_results_2)



