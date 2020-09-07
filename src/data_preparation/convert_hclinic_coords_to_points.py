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
from src.helper_functions.data_preparation_helper_functions import report_null_values

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

#%% --- EDA: Missing Values Exploration ---

hclinic_gdf_null_report = report_null_values(hclinic_gdf)
#We have two missing values here in in_district_eng column:
#However, as our dataset is really small, i want to protect as much
#values as possible.

#Create a missing data mask
missing_data_mask = hclinic_gdf.isnull().any(axis = 1) #.any is used to get rows from a multidimensional nan matrix
missing_data_clinic_names = hclinic_gdf.loc[missing_data_mask, "hclinic_name"]

#We'll insert the missing location info by hand. They are at Atasehir and Bakirkoy respectively.
hclinic_gdf.iloc[23,-1] = "Atasehir"
hclinic_gdf.iloc[25,-1] = "Bakirkoy"


#%% --- EDA: Datatype Agreement ---

hclinic_gdf_data_types = hclinic_gdf.dtypes
#Everything is as expected.

#%% --- EDA: Replicate Values ---

institution_name_counts = hclinic_gdf["hclinic_name"].value_counts()
for institution_appearance_number in institution_name_counts:
    assert(institution_appearance_number == 1)
    
#%% --- EDA: check for values outside polygons ---

#We've done a point-in-polygon query before and could find where each
#hair transplant center was located in.

#However, the map above shows that we've mis-labeled two hair transplant
#centers.
#Let's discover which ones they are:
    
polygons = istanbul_districts.geometry

not_in_any_polygon = []
for row in hclinic_gdf.iterrows():
    row_name = row[1]["hclinic_name"]
    row_geometry = row[1]["geometry"]
    in_any = False
    for polygon in polygons:
        if row_geometry.within(polygon):
            in_any = True
    if in_any == False:
        not_in_any_polygon.append((row_name, row_geometry))

#Since our only means of programatically determining where each transplant center is,
#we'll drop these two centers.

#Use mask to get index, then drop by index.
for center_tuple in not_in_any_polygon:
    hclinic = center_tuple[0]
    to_drop_mask = hclinic_gdf.loc[:,"hclinic_name"] == hclinic
    hclinic_gdf.drop(hclinic_gdf.index[to_drop_mask], inplace = True)
#%% --- Export Data ---
#Let's now export the file that we have created:
    
out_fp = Path("../../data/processed/hair_clinics_processed.shp")
hclinic_gdf.to_file(out_fp,encoding='utf-8-sig')




