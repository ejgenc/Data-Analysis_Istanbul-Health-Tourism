# -*- coding: utf-8 -*-
"""
------ What is this file? ------

This script targets three files:
    - istanbul_airbnb_processed_shapefile.shp
    - istanbul_districts.shp
    - district_income.xlsx
    
The script analyzes the geographic distribution of airbnb rentals at
the district level while also adding some extra information for further
bivariate correlation analysis.

Returns geographic_distribution_of_airbnb_rentals.shp
"""
#%% --- Import Required Packages ---

import os
from pathlib import Path # To wrap around filepaths
import pandas as pd
import geopandas as gpd
#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Import Data ---

#Import district data
import_fp = Path("../../data/external/istanbul_districts.shp")
districts_gdf = gpd.read_file(import_fp, encoding = "utf-8-sig")

#Import airbnb rental data
import_fp = Path("../../data/processed/istanbul_airbnb_processed_shapefile.shp")
airbnb_gdf= gpd.read_file(import_fp, encoding = "utf-8-sig")

#Import extra data
import_fp = Path("../../data/external/district_income.xlsx")
extra_data = pd.read_excel(import_fp, engine = "openpyxl")

#%% --- Aggregate airbnb count per district ---

airbnb_count_per_district = airbnb_gdf.loc[:,"district_e"].value_counts().rename_axis('district_e').reset_index(name='airbnb_count')

#%% --- Join in with district data ---

districts_gdf = districts_gdf.merge(airbnb_count_per_district,
                                              on = "district_e",
                                              how = "left")

#%% --- Subset only the info that you might need from districts_gdf ---

columns_to_drop = ["OBJECTID", "Shape_Leng", "Shape_Area",
                   "continent"]
districts_gdf.drop(columns_to_drop, axis = 1, inplace = True)

#%% --- Add in extra data ---

extra_data.rename(columns = {"district_eng" : "district_e"}, inplace = True)
districts_gdf = districts_gdf.merge(extra_data.loc[:,["district_e", "population", "yearly_average_household_income"]],
                                               on = "district_e",
                                               how = "left")

#%% --- Export data ---

export_fp = Path("../../data/final/geographic_distribution_of_airbnb_rentals.shp")
districts_gdf.to_file(export_fp, encoding = "utf-8")