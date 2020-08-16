# -*- coding: utf-8 -*-
"""
------ What is this file? ------

This script targets the istanbul_airbnb_raw.csv file. It cleans the .csv
file in order to prepare it for further analysis
           
"""
#%% --- Import Required Packages ---

import os
from pathlib import Path # To wrap around filepaths
import numpy as np
import pandas as pd

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Import Data ---

import_fp = Path("../../data/raw/istanbul_airbnb_raw.csv")
airbnb = pd.read_csv(import_fp, encoding='utf-8-sig')

#%% ---  Get a general sense of the datasets ---

# Shape of the data 
print(airbnb.shape) # 16251 rows, 16 cols

# First few lines
print(airbnb.head())

#Not much info, let's print the columns
airbnb_columns = airbnb.columns

#%% --- Clean the dataset: Relevant - Irrelevant Columns ---

airbnb_unwanted_columns = ["neighbourhood_group", "last_review", "number_of_reviews",
                           "minimum_nights",
                           "reviews_per_month",
                           "calculated_host_listings_count",
                           "availability_365"]

#Drop unwanted columns
airbnb.drop(columns = airbnb_unwanted_columns,
                        axis = 1,
                        inplace = True)  
    
# Check shape now
print(airbnb.shape) # 16251 rows, 9 cols

#%% --- Clean the dataset: Further Troubleshooting ---

#I want to be able to randomly take n samples from each dataset and then print them
#on a clean format to see the potential problems




# Sample from the datasets
#If i had something to test for, i'd strive for somewhat of a representative sample size
#while sampling. However, i think the best to do here would be to print what i can read
#because i don't have any computational measure to test for something:
airbnb_sample = airbnb.sample(20)

# Make some kind of a sample reader function
def sample_reader(dataframe):
    #Accepts a dataframe as an argument
    #Prints out the sample dataframe into the console in a column - by - column format
    dataframe_columns = dataframe.columns
    for column in dataframe_columns:
        print("Commencing with " + column + " column of the dataframe")
        print("")
        for i in range(0,len(dataframe)):
            selection = dataframe.iloc[i]
            print(str(selection[column]).encode("utf-8-sig"))
            print("")
            

sample_reader(airbnb_sample)

#SPOTTED PROBLEMS:
#   dataframe airbnb column neigborhood is not properly formatted:
#       Formatting fixes
#       should actually be called "district_tr"
#       There should be an accompanying "district_eng" column.

#%% --- Fix column naming ---

#I can use either dataframe.columns attribute to assign new columns
#or i can pass a dictionary with old names/new names into dataframe.rename()
airbnb_columns_in_english = ["listing_id", "name", "host_id", "host_name", "district_eng",
                             "latitude", "longitude", "room_type", "price"]
airbnb.columns = airbnb_columns_in_english 

#%% --- Add a new "district_tr" column

airbnb.loc[:,"district_tr"] = airbnb.loc[:,"district_eng"].str.lower().str.capitalize()  

#I will be using df.map() method, so i'll need two dataframes: one for existing values - tr values
#and one for exixsting values - eng values
unique_districts_tr_corrected = ["Kadıköy", "Fatih", "Tuzla", "Gaziosmanpaşa",
                                 "Üsküdar", "Adalar", "Sarıyer", "Arnavutköy",
                                 "Silivri", "Çatalca", "Küçükçekmece", "Beyoğlu",
                                 "Şile", "Kartal", "Şişli", "Beşiktaş", "Kağıthane",
                                 "Esenyurt", "Bahçelievler", "Avcılar", "Başakşehir",
                                 "Sultangazi", "Maltepe", "Sancaktepe", "Beykoz",
                                 "Büyükçekmece", "Bakırköy", "Pendik", "Bağcılar",
                                 "Esenler", "Beylikdüzü", "Ümraniye", "Eyüpsultan",
                                 "Çekmeköy", "Ataşehir", "Sultanbeyli", "Zeytinburnu",
                                 "Güngören", "Bayrampaşa"]

unique_districts_eng_corrected = ["Kadikoy", "Fatih", "Tuzla", "Gaziosmanpasa",
                                 "Uskudar", "Adalar", "Sariyer", "Arnavutkoy",
                                 "Silivri", "Catalca", "Kucukcekmece", "Beyoglu",
                                 "Sile", "Kartal", "Sisli", "Besiktas", "Kagithane",
                                 "Esenyurt", "Bahcelievler", "Avcilar", "Basaksehir",
                                 "Sultangazi", "Maltepe", "Sancaktepe", "Beykoz",
                                 "Buyukcekmece", "Bakirkoy", "Pendik", "Bagcilar",
                                 "Esenler", "Beylikduzu", "Umraniye", "Eyup",
                                 "Cekmekoy", "Atasehir", "Sultanbeyli", "Zeytinburnu",
                                 "Gungoren", "Bayrampasa"]


airbnb_unique_districts_dict_tr = dict(zip(unique_districts_eng_corrected, unique_districts_tr_corrected))
airbnb.loc[:,"district_tr"] = airbnb.loc[:,"district_tr"].map(airbnb_unique_districts_dict_tr)

#%% --- Export Data ---

export_fp = Path("../../data/processed/istanbul_airbnb_processed.csv")
airbnb.to_csv(export_fp,
              encoding='utf-8-sig',
              index = False)
