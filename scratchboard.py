# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 19:51:42 2020

@author: ejgen
"""

import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, MultiPoint, LineString, Polygon
from shapely.ops import nearest_points
from geopy import distance
import matplotlib.pyplot as plt
from src.helper_functions import data_analysis_helper_functions as functions

#%% --- Create test data ---
#%%     --- Mock DataFrame ---

#Create a random seed
np.random.seed([3,1415])
#Create a dataframe from random np numbers
test_df = pd.DataFrame(np.random.randint(10, size=(100, 5)),
                       columns=list('ABCDE'))
#Select ten percent of each column and turn it into np.nan
for col in test_df.columns:
    test_df.loc[test_df.sample(frac=0.1).index, col] = np.nan
    
#%%     --- Mock GeoDataFrame ---

random_points_basis_x = np.random.randint(low = 20, high = 40, size = 100)
random_points_basis_x_2 = np.random.randint(low = 25, high = 35, size = 100)
random_points_basis_y = np.random.randint(low = 20, high = 40, size = 100)
random_points_basis_y_2 = np.random.randint(low = 25, high = 35, size = 100)
random_points = [Point(x,y) for (x,y) in zip(random_points_basis_x,random_points_basis_y)]
random_points_2 = [Point(x,y) for (x,y) in zip(random_points_basis_x_2,random_points_basis_y_2)]

test_gdf_1 = gpd.GeoDataFrame(test_df.copy(),
                            geometry = random_points,
                            crs = "EPSG:4326")

test_gdf_2 = gpd.GeoDataFrame(test_df.copy(),
                            geometry = random_points_2,
                            crs = "EPSG:4326")

result = functions.nearest_neighbor_analysis(test_gdf_1,
                                             test_gdf_2)

links = [LineString([p1,p2]) for p1, p2 in result.loc[:,["point_of_origin","nearest_point"]].values]

links_gseries = gpd.GeoSeries(links,
                              crs = test_gdf_1.crs)

result["links"] = links_gseries

# Scheme quantiles?
# IS THIS REALLY THE RIGHT WAY TO DO THIS?
fig = plt.figure(figsize = (10,10))
ax_1 = fig.add_subplot(1,1,1)


for spine in ax_1.spines:
    ax_1.spines[spine].set_visible(False)

ax_1.xaxis.set_visible(False)
ax_1.yaxis.set_visible(False)
    
color_1 = "#599CCF"
color_2 = "#E4784D"
color_3 = "#1CB2FE"
color_4 = "#F68C69"
color_5 = "#1A1C1A"

fig.set_facecolor(color_5)
ax_1.set_facecolor(color_5)

result.set_geometry("links", inplace = True)
result.plot(ax = ax_1,
                    color = "white",
                    alpha = 1,
                    lw=2)

result.set_geometry("point_of_origin", inplace = True)
result["point_of_origin"].plot(ax = ax_1,
                               color = color_3,
                               alpha = 1,
                               zorder = 2,
                               markersize = 50,
                               marker = "o")

result.set_geometry("nearest_point", inplace = True)
result["nearest_point"].plot(ax = ax_1,
                             color = color_4,
                             zorder = 3,
                             alpha = 1,
                             markersize = 50,
                             marker = "^")

#result.set_geometry("links", inplace = True)
# result.plot(ax = ax_1,
#                     column = "distance_in_meter",
#                     cmap = "Purples",
#                     alpha=1,
#                     lw=2)



plt.savefig("test.png")


