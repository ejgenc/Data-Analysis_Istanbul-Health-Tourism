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
from shapely.geometry import Point

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Import Data ---

# #Import hair clinics data
# import_fp = Path("../../data/processed/hair_clinics_processed.shp")
# hclinics_gdf = gpd.read_file(import_fp)

# #Import aesthethic centers data
# import_fp = Path("../../data/processed/istanbul_aesthethic_centers_processed_shapefile.shp")
# acenters_gdf = gpd.read_file(import_fp)

#%% --- MORE ---


