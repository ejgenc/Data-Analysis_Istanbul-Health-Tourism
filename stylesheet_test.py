# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 15:33:46 2020

@author: ejgen
"""

#%% -- Import packages ---

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

#%% --- Create some random data ---

#Create a random seed
np.random.seed([3,1415])
#Create a dataframe from random np numbers
test_df = pd.DataFrame(np.random.randint(10, size=(100, 5)),
                       columns=list('ABCDE'))
#Select ten percent of each column and turn it into np.nan
for col in test_df.columns:
    test_df.loc[test_df.sample(frac=0.1).index, col] = np.nan
    
#%% --- Init stylesheet and plot ---

with plt.style.context('src/data_visualization/matplotlib_stylesheet_ejg_fixes'):
    fig = plt.figure(figsize = (10,10))
    ax = fig.add_subplot(1,1,1)
    ax.scatter(test_df["A"], test_df["B"])
    
#%% --

with plt.style.context('src/data_visualization/matplotlib_stylesheet_ejg_darkmode'):
    fig = plt.figure(figsize = (10,10))
    ax = fig.add_subplot(1,1,1)
    ax.scatter(test_df["A"], test_df["B"])
    
#%% 

with plt.style.context(["src/data_visualization/matplotlib_stylesheet_ejg_fixes",
                        'src/data_visualization/matplotlib_stylesheet_ejg_darkmode']):
    fig = plt.figure(figsize = (10,10))
    ax = fig.add_subplot(1,1,1)
    ax.scatter(test_df["A"], test_df["B"])
    
    
#%%

with plt.style.context('src/data_visualization/matplotlib_stylesheet_ejg_fixes'):
    fig = plt.figure(figsize = (10,10))
    ax = fig.add_subplot(1,1,1)
    sns.distplot(test_df["A"],
                 ax = ax)


#%% 

with plt.style.context(["src/data_visualization/matplotlib_stylesheet_ejg_fixes",
                        'src/data_visualization/matplotlib_stylesheet_ejg_darkmode']):
    fig = plt.figure(figsize = (10,10))
    ax = fig.add_subplot(1,1,1)
    sns.distplot(test_df["A"],
                 ax = ax)
