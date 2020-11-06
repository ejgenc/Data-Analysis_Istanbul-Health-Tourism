# -*- coding: utf-8 -*-
"""
------ What is this file? ------

This script targets seven files:
    - nn_analysis_results_all.csv
    - nn_analysis_results_normalized.csv
    - nn_analysis_results_norm_atasehir.csv
    - nn_analysis_results_norm_besiktas.csv
    - nn_analysis_results_norm_kadikoy.csv
    - nn_analysis_results_norm_sisli.csv
    - nn_analysis_results_norm_uskudar.csv
    
The script produces scatterplots that show Pearson'r and Spearman's rho
analysis results for each nearest neighbor result dataset. The relations
are calculated to see whether closeness to a health tourism center
affects price in some way.

Returns single and small multiple scatterplots.

"""
#%% --- Import Required Packages ---

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Import Data ---

#%% --- Visualizations ---

#%% --- Export Figures ---
