# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 16:12:37 2020
@author: ejgen

------ What is this file? ------
                
This file is used to scrape the web for information about the hair transplant
centers that can be found in Istanbul.

I use simple html and xpath scraping to get a list of the potential hair transplant
centers in Istanbul. Then, i use Selenium to automate Google Maps coordinate extraction.

I then use an Istanbul shapefile and conduct point - in - polygon query to induce
which district each clinic belongs to.

Lastly, i turn all of this into a Pandas Dataframe so that i can save it as a CSV

"""

#%% --- Import required packages ---

import requests # To request for an HTML file
from lxml import html #To create the document tree / xpath query
from selenium import webdriver
import pandas as pd
import geopandas as gpd #A module built on top of pandas for geospatial analysis
import matplotlib.pyplot as plt #For plotting
from pyproj import CRS #For CRS (Coordinate Reference System) functions
from shapely.geometry import Point, MultiPoint #Required for point/polygon geometry


#%% --- Scrape the hair transplant clinic names from the web ---

#Open a request to the page
page = requests.get("https://www.sacekimiburada.com/istanbul-sac-ekim-merkezleri")

#Create an html document tree of the page content
tree = html.fromstring(page.content)

#Parse the tree using xpath to find the information we are looking for
hclinic_names_unmodified = list(tree.xpath('//h3/text()'))

#Convert to string and add to list using list comprehension
hclinic_names = [str(s) for s in hclinic_names_unmodified]

#Exclude some faulty rows 
hclinic_names = hclinic_names[3:-3]

#%% --- Turn hair clinic names into a dataframe ---

hclinic_df = pd.DataFrame(hclinic_names, columns = ["hclinic_name"])

#Some correction

hclinic_df.loc[0,"hclinic_name"] = "Aesthetic Hairtrans Saç Ekim Merkezi"

#%% --- Add a "hclinic_search_url" column ---

#Creae a search url string
search_url = "https://www.google.com/maps/search/"

#Concat with each row to create a search url belonging to that row
hclinic_df["hclinic_search_url"] = search_url + hclinic_df["hclinic_name"]

#%% --- Scrape the location data with Selenium and Google Maps ---

#We'll be scraping the Google Maps web interface with Selenium.

#Create an empty list where coordinates will be stored
Url_With_Coordinates = []

#Access the options for Chrome webdrivers
option = webdriver.ChromeOptions()

#Add some exceptions to deactivate images and javascript
#This way, the page will load faster.
prefs = {'profile.default_content_setting_values': {'images':2, 'javascript':2}}
option.add_experimental_option('prefs', prefs)

#Initiate the Google Chrome webdriver with options.
driver = webdriver.Chrome("selenium chrome driver/chromedriver.exe", options=option)

for url in hclinic_df.loc[:,"hclinic_search_url"].values:
    driver.get(url) #Go to the page
    
    #Select the html element containing coords info via css selector
    raw_str = driver.find_element_by_css_selector('meta[itemprop=image]').get_attribute('content')
    
    # Split to format - 1
    processed_str_1 = raw_str.split('?center=')[1]
    
    #Split to format - 2
    processed_str_2 = processed_str_1.split('&zoom=')[0]
    
    #Split to format - 3
    processed_str_3 = processed_str_2.split("%2C")
    
    #Get tuple position 0 as latitude and tuple position 1 as longitude
    lat = processed_str_3[0]
    lon = processed_str_3[1]

    Url_With_Coordinates.append((lat,lon))

driver.close()

#%% --- Write URL_with_Coordinates info into the dataframe ---

#To keep things nice and steady, we will now need to pass all this into
#our hclinic_df DataFrame. This will be quite straightforward as the list that
#we have was constructed in the same order as our dataframe.

#Create a joint lat_lon column from Url_With_Coordinates list
hclinic_df["lat_lon"] = Url_With_Coordinates

#Create a list out of each tuple in the lat_lon column, convert them to a dataframe with two cols
#and assign the cols to lat and lot respectively.
hclinic_df[["lat", "lon"]] = pd.DataFrame(hclinic_df["lat_lon"].tolist(), index = hclinic_df.index)

#Convert these to float

hclinic_df[["lat", "lon"]] = hclinic_df[["lat", "lon"]].astype(float)


#Delete the lat_lon column

hclinic_df.drop(labels = "lat_lon",
                axis = 1,
                inplace = True)

#Delete some specific indexes that do not fit

unwanted_hclinic_names = ["Dr. Yaman Hair Clinic","Prens Hair",
                          "Marmara Hair Clinic","Life Point","Dr.Eser Aydoğdu",
                          "MepyyHair"]

unwanted_hclinic_names_mask = hclinic_df.loc[:,"hclinic_name"].isin(unwanted_hclinic_names) == False

hclinic_df = hclinic_df.loc[unwanted_hclinic_names_mask,:]

#%% --- Write the Dataframe as a CSV ---
# It's a nice idea to have a copy of our data at this point.

out_fp = "../../../Data/Non-GIS data/raw/istanbul_hair_clinics.csv"

#Commented out to prevent accidental rewriting
#hclinic_df.to_csv(out_fp, encoding='utf-8-sig', index = False)


#%%
#We are done with the Dataframe.
#Let's now move to point - in - polygon analysis using Geopandas

#%% --- Import our Istanbul shapefile ---

istanbul_districts_fp = "../../Data/GIS data/Processed/istanbul_districts.shp"
istanbul_districts = gpd.read_file(istanbul_districts_fp)

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
    pip_mask = hclinic_gdf.within(district_mask["geometry"])
    
    hclinic_gdf.loc[pip_mask,"in_district_e"] = district_name
    
#We had to resort to the use of df.iloc[] in above code because
#plain boolean masks did not play along well with the code.   
#%% --- Exporting the file ---
#Let's now export the file that we have created:
    
out_fp = "../../../Data/GIS data/Processed/istanbul_hair_clinics_cleaned.shp"

#Commented out to prevent accidental re-writing
#hclinic_gdf.to_file(out_fp)




