# -*- coding: utf-8 -*-
"""
------ What is this file? ------

This script targets eight files
    - nn_analysis_results_all.csv
    - nn_analysis_results_normalized.csv
    - nn_analysis_results_norm_atasehir.csv
    - nn_analysis_results_norm_besiktas.csv
    - nn_analysis_results_norm_kadikoy.csv
    - nn_analysis_results_norm_sisli.csv
    - nn_analysis_results_norm_uskudar.csv
    
The script produces abstract maps to confirm nearest neighbor analysis.
In the maps, each orange triangle represents a health tourism center.
Each blue circle represents an Airbnb rental.
The lines in between the two symbols(triangles and circles) show which
health tourism center is closest to which Airbnb.
A succesful NN search would result in each circle being connected to
only the nearest triangle, which would be visible in the visualization.

Returns eight abstract maps that attempt to confirm nearest neighbor analysis
for different datsets.
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

#Istanbul districts for reference crs
import_fp = Path("../../data/external/istanbul_districts.shp")
istanbul_districts = gpd.read_file(import_fp)

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
    
#%% --- Visualize the results of NN analysis for confirmation ---

fig_1 = confirm_nearest_neighbor_analysis(nn_analysis_results_all_gdf)

fig_2 = confirm_nearest_neighbor_analysis(nn_analysis_results_normalized_gdf)

per_district_confirmation_plot = []
for district_gdf in nn_analysis_results_per_district_gdf.values():
    conf_fig = confirm_nearest_neighbor_analysis(district_gdf)
    per_district_confirmation_plot.append(conf_fig)
    
#%% --- Export data ---

current_filename_split = os.path.basename(__file__).split(".")[0].split("_")
current_filename_complete = "_".join(current_filename_split)

mkdir_path = Path("../../media/figures/raw/{}".format(current_filename_complete))
os.mkdir(mkdir_path)

figures = [plot for plot in per_district_confirmation_plot]
figures.extend([fig_1,fig_2])

filenames = ["confirmation_all_norm_atasehir",
             "confirmation_all_norm_besiktas",
             "confirmation_all_norm_kadikoy",
             "confirmation_all_norm_sisli",
             "confirmation_all_norm_uskudar",
             "confirmation_all",
             "confirmation_all_normalized",]

for figure, filename in zip(figures, filenames):
    filename_extended = filename + ".png"
    export_fp = Path.joinpath(mkdir_path, filename_extended)
    figure.savefig(export_fp,
                    pad_inches = 0,
                    dpi = 300,
                    bbox_inches = "tight")