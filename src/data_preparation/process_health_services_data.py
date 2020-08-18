# -*- coding: utf-8 -*-
"""
------ What is this file? ------

This script targets the istanbul_healthservices_raw.csv file. It cleans the .csv
file in order to prepare it for further analysis.
           
"""
#%% --- Import Required Packages ---

import os
from pathlib import Path # To wrap around filepaths
import re #RegEx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.data_preparation.data_preparation_helper_functions import report_null_values
from src.data_preparation.data_preparation_helper_functions import plot_null_values_matrix

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Import Data ---

import_fp = Path("../../data/raw/istanbul_healthservices_raw.csv")
hservices = pd.read_csv(import_fp, encoding='utf-8-sig')

#%% --- EDA: Determine and drop irrelevant columns for first round ---

df_columns = hservices.columns

#Information related to icu, n#_beds, ambulance and care_type is not needed.

columns_to_drop = ["icu", "n#_beds", "ambulance", "care_type"]
hservices.drop(labels = columns_to_drop,
                           axis = 1,
                           inplace = True)

#%% --- EDA: Explore Missing Values ---

plot_null_values_matrix(hservices)

#The number of missing values appears to be either 0 or insignificant.
#Let's tackle this numerically:
    
report_null_values(hservices, print_results = True)

#There are some missing values, but none in important columns such as lat/long and
#name.
#Since the numbers are insignificant, we can drop the very few rows that have missing values.

#%% --- Drop rows with missing values ---

hservices.dropna(axis = 0,
                 inplace = True)
#%% --- Encode information about being related to health tourism ---

#Aesthetic surgery centers will be considered related to health tourism.
#This script encodes information about whether an institution is related to
#health tourism or not by looking at institution name.

#Reset the related_t_htourism column of all rows
hservices.loc[:,"related_to_htourism"] = False

#Create a list of RegEX patterns that can catch aesthethic centers
regex_patterns = [r"\b[Ee]st\w+\b", r"\b[Pp]last\w+\b",
                  r"\b[Ae]st\w+\b", r"\bAest\w+\b"]

#Loop over regex patterns to classify as Related/Unrelated
#Can also be implemented with df.mask()
for pat in regex_patterns:
    pat_mask = hservices.loc[:,"institution_name"].str.contains(pat,
                                                                 flags = re.I)
    selection = hservices.loc[pat_mask, "related_to_htourism"] = True
    
#%% --- Drop a second round of columns ---

columns_to_drop = ["institution_id","institution_type","address",
                   "neighborhood_tr","institution_type_eng","institution_type_abbrv_tr",
                   "institution_type_abbrv_eng"]

hservices.drop(labels = columns_to_drop,
                           axis = 1,
                           inplace = True)

#%% --- Keep only the rows that are related to health tourism ---

htourism_mask = hservices.loc[:,"related_to_htourism"] == True
hservices = hservices.loc[htourism_mask,:]

hservices.drop(labels = "related_to_htourism",
                           axis = 1,
                           inplace = True)

#%% --- Export Data ---

export_fp = Path("../../data/processed/istanbul_aesthethic_centers_processed.csv")
hservices.to_csv(export_fp,
                 encoding = "utf-8-sig",
                 index = False)
    



    
    