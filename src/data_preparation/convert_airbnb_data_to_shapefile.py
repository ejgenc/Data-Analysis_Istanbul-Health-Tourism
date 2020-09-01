# -*- coding: utf-8 -*-
"""
------ What is this file? ------

This script targets the istanbul_airbnb_processed.csv file.
It converts the file into a shapefile.        
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
import_fp = Path("../../data/processed/istanbul_airbnb_processed.csv")
airbnb_df = pd.read_csv(import_fp, encoding = "utf-8-sig")

#also import secondary dataset
import_fp = Path("../../data/processed/hair_clinics_processed.shp")
hclinics_gdf = gpd.read_file(import_fp)

#%% --- Convert airbnb_df DataFrame to a GeoDataFrame ---

#Use the crs of hclinics_gdf as reference crs
reference_crs = hclinics_gdf.crs
#Convert latitude and longitude information of airbnb_df into Shapely point objects.
geometry = [Point(xy) for xy in zip(airbnb_df["latitude"], airbnb_df["longitude"])]
#convert airbnb_df to a GeoDataframe with crs as reference crs and geometry as geometry
airbnb_gdf = gpd.GeoDataFrame(airbnb_df,
                              crs = reference_crs,
                              geometry = geometry)

#%% --- Export airbnb_gdf as a shapefile ---

export_fp = Path("../../data/processed/istanbul_airbnb_processed_shapefile.shp")
airbnb_gdf.to_file(export_fp, encoding = "utf-8-sig")


