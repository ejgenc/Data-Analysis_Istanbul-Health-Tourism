# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 16:12:37 2020
@author: ejgen

------ What is this file? ------
                
This file is used to scrape the web for information about the hair transplant
centers that can be found in Istanbul.

I use simple html and xpath scraping to get a list of the potential hair transplant
centers in Istanbul. Then, i use Selenium to automate Google Maps coordinate extraction.

Finally, the dataset that contains information about clinic name - clinic search url
and clinic-coordinate is written to a csv file.
"""

#%% --- Import required packages ---

import os
import requests # To request for an HTML file
from lxml import html #To create the document tree / xpath query
from selenium import webdriver # For webscraping
from pathlib import Path # To wrap around filepaths
import pandas as pd

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


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

#%% --- Drop rows that come after a certain iloc ---

last_row_mask = hclinic_df.loc[:,"hclinic_name"] == "Dr.İbrahim AŞKAR"
last_row_index = hclinic_df.loc[last_row_mask].index[0]

after_last_row_mask = hclinic_df.index <= last_row_index
hclinic_df = hclinic_df[after_last_row_mask]


#%% --- Add a "hclinic_search_url" column ---

#Create a search url string
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
                          "MepyyHair", "Equinox Hair", "Hairworld İstanbul"]

unwanted_hclinic_names_mask = hclinic_df.loc[:,"hclinic_name"].isin(unwanted_hclinic_names) == False

hclinic_df = hclinic_df.loc[unwanted_hclinic_names_mask,:]

#%% --- Export Data ---
out_fp = Path("../../data/raw/hair_clinics_raw.csv")
hclinic_df.to_csv(out_fp, encoding='utf-8-sig', index = False)




