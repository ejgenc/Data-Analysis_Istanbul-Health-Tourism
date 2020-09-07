# -*- coding: utf-8 -*-
"""
------ What is this file? ------

This script targets the istanbul_aesthethic_centers_processed.csv file.
It converts the file into a shapefile in order to further prepare it for merging.           
"""
#%% --- Import Required Packages ---

import os
from pathlib import Path # To wrap around filepaths
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Import Data ---

#import the primary dataset
import_fp = Path("../../data/processed/istanbul_aesthethic_centers_processed.csv")
acenters_df = pd.read_csv(import_fp, encoding = "utf-8-sig")

#also import secondary dataset
import_fp = Path("../../data/processed/hair_clinics_processed.shp")
hclinics_gdf = gpd.read_file(import_fp)
#%% --- Convert acenters_df into a geodataframe ---

#Get the crs of reference from hclinics_gdf
reference_crs = hclinics_gdf.crs
#Convert latitude and longitude information from acenters_df into points
geometry = [Point(xy) for xy in zip(acenters_df["longitude"],acenters_df["latitude"])]
#Conver acenters_df to gdf with crs as reference_crs and geometry as geometry
acenters_gdf = gpd.GeoDataFrame(acenters_df,
                                crs = reference_crs,
                                geometry = geometry)
#%% -- Export Data ---
export_fp = Path("../../data/processed/istanbul_aesthethic_centers_processed_shapefile.shp")
acenters_gdf.to_file(export_fp, encoding = "utf-8-sig")
