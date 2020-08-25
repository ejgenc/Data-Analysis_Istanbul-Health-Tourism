# -*- coding: utf-8 -*-
"""
------ What is this file? ------
                
This script targets the hair_clinics_raw.csv file. The script encodes information
about the district each hair clinic belongs to before saving it as a shapefile
with appropriate CRS information.

"""

#%% --- Import Required Packages ---

import os
from pathlib import Path # To wrap around filepaths
import pandas as pd
import geopandas as gpd #A module built on top of pandas for geospatial analysis
from pyproj import CRS #For CRS (Coordinate Reference System) functions
from shapely.geometry import Point #Required for point/polygon geometry
import matplotlib.pyplot as plt

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


#%% --- Import Data ---

#Import Istanbul districts data
istanbul_districts_fp = Path("../../data/external/istanbul_districts.shp")
istanbul_districts = gpd.read_file(istanbul_districts_fp)

#Import hair clinic data
hclinic_fp = Path("../../data/raw/hair_clinics_raw.csv")
hclinic_df = pd.read_csv(hclinic_fp, encoding='utf-8-sig')

#%% --- Make the hclinic_df into a geopandas file ---

#Two GeoDataFrames must share the same CRS (Coordinate Reference System)
#for any meaningful analysis to occur.

reference_crs = istanbul_districts.crs

#We also need to convert lat lon to points:
    
geometry = [Point(xy) for xy in zip(hclinic_df['lon'], hclinic_df['lat'])]

hclinic_gdf = gpd.GeoDataFrame(hclinic_df,
                                crs = reference_crs,
                                geometry = geometry)


#Run some checks
print(hclinic_gdf.crs == reference_crs)


#%% --- Check it on the map ---

#It's always a nice idea to check all this on a map to see if it works in practice:
    
fig = plt.figure(figsize = (8,8))

ax = fig.add_subplot(1,1,1)

istanbul_districts.plot(ax = ax,
                        color = "blue")
hclinic_gdf.plot(ax = ax,
                      color = "red")

#%% --- Perform point - in - polygon query for each district
#I also want to encode information about the district each hair clinic belongs to
#I can do this using a simple point in polygon query.
#For each polygon in istanbul_districts, i will create a boolean index
#and use that boolean index to flag the values that are in that polygon
#as belonging to that polygon.

district_index_list = istanbul_districts.index.tolist()

for district_index in district_index_list:
    district_name = istanbul_districts.iloc[district_index]["district_e"]
    district_mask = istanbul_districts.iloc[district_index]
    p_in_p_mask = hclinic_gdf.within(district_mask["geometry"])
    
    hclinic_gdf.loc[p_in_p_mask,"in_district_eng"] = district_name
    
#We had to resort to the use of df.iloc[] in above code because
#plain boolean masks did not play along well with the code.
   
#%% --- Export Data ---
#Let's now export the file that we have created:
    
out_fp = Path("../../data/processed/hair_clinics_processed.shp")
hclinic_gdf.to_file(out_fp,encoding='utf-8-sig')




