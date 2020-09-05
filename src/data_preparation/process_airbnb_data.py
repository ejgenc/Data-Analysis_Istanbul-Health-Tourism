# -*- coding: utf-8 -*-
"""
------ What is this file? ------

This script targets the istanbul_airbnb_raw.csv file. It cleans the .csv
file in order to prepare it for further analysis
           
"""
#%% --- Import Required Packages ---

import os
import pathlib
from pathlib import Path # To wrap around filepaths
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.stats import iqr
from src.helper_functions.data_preparation_helper_functions import sample_and_read_from_df
from src.helper_functions.data_preparation_helper_functions import report_null_values

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

#If i had something to test for, i'd strive for somewhat of a representative sample size
#while sampling. However, i think the best to do here would be to print what i can read
#because i don't have any computational measure to test for something:

sample_and_read_from_df(airbnb, 20)

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

#%% --- One-off fix for districts named "Eyup" ---

eyup_mask = airbnb.loc[:,"district_eng"] == "Eyup"

airbnb.loc[eyup_mask, "district_eng"] = "Eyupsultan"
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
                                 "Esenler", "Beylikduzu", "Umraniye", "Eyupsultan",
                                 "Cekmekoy", "Atasehir", "Sultanbeyli", "Zeytinburnu",
                                 "Gungoren", "Bayrampasa"]


airbnb_unique_districts_dict_tr = dict(zip(unique_districts_eng_corrected, unique_districts_tr_corrected))
airbnb.loc[:,"district_tr"] = airbnb.loc[:,"district_tr"].map(airbnb_unique_districts_dict_tr)

#%% --- EDA: Explore Missing Values ---

#Let's check null values first
null_report = report_null_values(airbnb)

#We have so few missing values, dropping them won't affect our quality at all.
# Let's do exactly that.

airbnb.dropna(axis = 0,
              inplace = True)

#%% --- EDA: Explore Datatype agreement ---

#Now, let's check data type agreement for each column.
data_types = airbnb.dtypes
# The data types with "object" warrant further investigation
#They could just be strings, but mixed data types also show as "object"

# Let's select "object" data types and query once again.
airbnb_dtype_object_only = airbnb.select_dtypes(include = ["object"])
print(airbnb_dtype_object_only.columns)
#As all the column names seem to accomodate only strings, we can be
#pretty sure that showing up as object is correct behavior.

#%% --- EDA - Explore Outliers in price ---

fig = plt.figure(figsize = (19.20, 10.80))
ax = fig.add_subplot(1,1,1)
ax.hist(x = airbnb.loc[:,"price"],
        bins = 20)

#Our histogram is very wonky. It's obvious that there are some issues. Let's see:
    
# It doesn't make sense for a airbnb room to cost 0 liras. That's for sure.
print(airbnb.loc[:,"price"].sort_values().head(20))

#What about maxes?
print(airbnb.loc[:,"price"].sort_values(ascending = False).head(30))
#There are some very high maxes, that's for sure. Let's try to make heads and tails of
#what these houses are:

possible_outliers = airbnb.sort_values(by = "price",
                                       axis = 0,
                                       ascending = False).head(30)

# A qualitative analysis of such houses show that there really aappears to be a problem
#with pricing. Let's calculate the IQR to drop the outliers:

#Calculate the iqr
price_iqr = iqr(airbnb.loc[:,"price"], axis = 0)

#Calculate q3 and q1
q1 = airbnb["price"].quantile(0.25)
q3 = airbnb["price"].quantile(0.75)

#Create min and max mask
min_mask = airbnb.loc[:,"price"] >= q1 - (1.5 * price_iqr)
max_mask = airbnb.loc[:,"price"] <= q3 + (1.5 * price_iqr)
#Combine masks
combined_mask = min_mask & max_mask
#Create subset
airbnb_within_iqr = airbnb.loc[combined_mask]

fig = plt.figure(figsize = (19.20, 10.80))
ax = fig.add_subplot(1,1,1)
ax.hist(x = airbnb_within_iqr.loc[:,"price"],
        bins = 20)

#Alright, limiting our data to an IQR appears to omit a whole lot of data.
#I am sure that some of the outliers we have are errors of entry.
#However, the only ones that we can conclusively prove are the entries that are rated at 0.
#We'll drop these

#Create a mask for zeros
zero_mask = (airbnb.loc[:,"price"] > 0)

#Filter using the mask
airbnb = airbnb.loc[zero_mask,:]


# #%% --- Export Data ---

export_fp = Path("../../data/processed/istanbul_airbnb_processed.csv")
airbnb.to_csv(export_fp,
              encoding='utf-8-sig',
              index = False)