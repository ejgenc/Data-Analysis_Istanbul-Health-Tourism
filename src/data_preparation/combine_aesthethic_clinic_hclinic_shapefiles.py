# -*- coding: utf-8 -*-
"""
------ What is this file? ------

This script targets two files:
    - hair_clinics_processed.shp 
    - istanbul_aesthethic_centers_processed_shapefile.shp
The script combines the two files into a joint shapefile.
"""
#%% --- Import Required Packages ---

import os
from pathlib import Path # To wrap around filepaths
import re #RegEx
import numpy as np
import pandas as pd
import geopandas as gpd
#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Import Data ---

#Import hair clinics data
import_fp = Path("../../data/processed/hair_clinics_processed.shp")
hclinics_gdf = gpd.read_file(import_fp)

#Import aesthethic centers data
import_fp = Path("../../data/processed/istanbul_aesthethic_centers_processed_shapefile.shp")
acenters_gdf = gpd.read_file(import_fp)

#%% --- Drop and rename hairclinic columns ---

# Drop URL column
hclinics_gdf.drop("hclinic_se",
                axis = 1,
                inplace = True)

#Rename certain columns
hclinics_gdf.rename(columns = {"hclinic_na" : "institution",
                             "in_distric": "district_eng",
                             "lat" : "latitude",
                             "lon" : "longitude"},
                                inplace = True)

#%% --- Drop and rename acenters_gdf columns ---

#Drop pub_or_priv column
acenters_gdf.drop("private_or",
                axis = 1,
                inplace = True)

#Rename certain columns
acenters_gdf.rename(columns = {"institutio" : "institution",
                             "district_e": "district_eng",
                             "district_t" : "district_tr"},
                                inplace = True)

#%% --- Extract district tr-eng info from acenters_gdf ---

#Dirty pandas coding to extract the info that i want
districts_tr_eng_valcounts = list(acenters_gdf.loc[:,["district_tr", "district_eng"]].value_counts().index)

#Compile the info into a dictionary
districts_dict = {y:x for x,y in districts_tr_eng_valcounts}

#%% --- Add district_tr information to hclinics_gdf

#Map using the information you've obtained before
hclinics_gdf.loc[:,"district_tr"] = hclinics_gdf.loc[:,"district_eng"].map(districts_dict)

#See what's missing
missing_districts_mask = hclinics_gdf.isnull().any(axis = 1) #.any() is really powerful
missing_districts = hclinics_gdf.loc[missing_districts_mask,["district_eng"]].value_counts()

#Manually write the Turkish versions
districts_tr = ["Ataşehir", "Beyoğlu", "Beylikdüzü",
                "Küçükçekmece", "Eyüpsultan", "Esenyurt", "Zeytinburnu",
                "Sultangazi", "Pendik", "Kartal", "Kağıthane", "Esenler",
                "Beykoz", "Avcılar"]

#Create a dict of district_eng keys and district_tr values
districts_tr_dict = {}
i = 0
for district in list(missing_districts.index):
    districts_tr_dict[district[0]] = districts_tr[i]
    i += 1

#Map over missing values.
hclinics_gdf.loc[missing_districts_mask,"district_tr"] = hclinics_gdf.loc[:,"district_eng"].map(districts_tr_dict)

#%% --- Combine acenters_gdf and hclinics_gdf ---
htourism_centers = hclinics_gdf.append(acenters_gdf)

#%% 
out_fp = Path("../../data/processed/htourism_centers_processed.shp")
htourism_centers.to_file(out_fp, encoding='utf-8-sig')
