# Data Analysis_Istanbul Health Tourism #

![Header]()

* * *

## External Links ##

**PUT EXTERNAL LINKS HERE**

## What is this project about? ##

A data analysis project that attempts to measure how much health tourism affects AirBnB rental prices in Istanbul.

**PUT PROJECT DESCRIPTION HERE**

## Technical Details ##

**PUT TECHNICAL DETAILS HERE**

* * *

## How to reproduce this project? ##

### Why reproducibility? ###

I believe that openness and ease of reproduction are two very important concepts that build a foundation of trust under the dissemination of knowledge. You can always consume the end result of my project, that is what most people do. However, there may be people who want to be able to re-create my analysis steps one by one. This is the reason why this project was built with reproducibility in mind.

### Methods of reproduction ###

Successful reproduction of a data science/analysis project requires the communication of the information that is related to the reproduction of the environment that the project was conducted in first. Only then can the analysis be replicated succesfully.  

#### 1.) Recreate the environment that the analysis was conducted in ####

The project files that i present offer two ways to do this for to account for the two most popular package managers for python, conda and pip. Let's start with the preferred method first:

##### a.) Using the environment.yml file with conda package manager #####

You can use this option if you have the conda package manager installed in your computer. The preferred method is to cd to the directory of the project and then run the following command in the Anaconda prompt (or any terminal where you can run conda from):

`conda env create -f environment.yml`

Running this command will make conda create a new environment similar to the environment of the analysis with the information provided inside the environment.yml file. When you run the command, you will be able to specify the name of this new environment. Once you are done, **don't forget to activate your environment before running the analysis.**

##### b.) Create the environment yourself and load the packages using the requirements.txt and pip #####

It is still possible to recreate the original environment if you are not using the conda package manager. The pip manager that comes with many Python installers is able to install requirements using the requirements.txt file present in the project. **However, you first need to create an environment yourself separate from you base Python environment so as to prevent potential problems** The process of creating a virtual environment through pip is lengthier than the method above. [Here's the official documentation of how to install packages and create virtual environments using pip.](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

Once you have created your environment, you can now install all the packages using the requirements.txt file. To do so, **activate your virtual environment**, cd to the project folder and run the following in a Python terminal:

`pip install --requirement requirements.txt`

**Now that we have recreated an environment similar to the one the project was created in, we can move on to reproducing the analysis.**

#### 2.) Utilize the Python doit package to replicate the analysis ####

[The doit package](https://pydoit.org/) is a handy tool in Python that can be used to automate certain tasks, including data analysis workflows. This project makes use of the doit package to make replication easier. The doit module was included in both of the dependency creation methods. All the information related to the doit package is located in the **dodo.py** file.

To run the whole cleaning, analysis and visualization process from start to finish, do the following:

* Open a Python interpreter or any command line tool you can run Python from

* Activate the environment you have created in the previous step

* cd to the project folder

* Simply run the following command: `doit`

## Project  Organization ##

Below is a document tree of this project for those who wish to explore further.

--------
```
    ├── LICENSE            < - License for the codes responsible in creating this data analysis projects.
    |
    ├── README.md          <- The top-level README for the users of this project.
    |
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── final          <- Data that has been analyzed.
    │   ├── processed      <- Cleaned and processed data ready to be analyzed.
    │   └── raw            <- The original, immutable data dump.
    │
    │
    ├── eda_notebooks      <- Jupyter notebooks that have data explorations. These files were not created with external viewers in mind.
    |                         You can explore them if you wish. However, a good viewing experience is not promised.
    |
    |
    |── media              <- Contains internally generated figures and external photos. Internally generated figures come with a license.
    |    ├── external_media <- Images and media downloaded from third party resources. A .txt file of references and attribution is included.
    │    ├── figures        <- Data visualizations generated through scripts
    |                                             
    |
    |
    ├── references         <- Data dictionaries, manuals, and all other explanatory material.
    │
    |
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    |
    |
    ├── src                         <- Source code for use in this project.
    │   |
    │   │
    │   ├── data_preparation        <- Scripts to download or generate data
    │   |
    |   |── data_analysis           <- Scripts to generate intermediary datasets to base visualizations on.                           
    |   |   
    │   |── data_visualization      <- Scripts to create visualizations.
    |   |
    |   |── helper_functions        <- Scripts that contain various helper functions.
    |   
    |
    │       
    ├── tests                       <- Contains test modules that test the data analysis pipeline.
    |   |
    |   ├── unit_tests              <- Contains unit tests. Folder structure mirrors that of the folder src.
    |   |         |
    |   |         |
    |   |         |── data_preparation 
    |   |         |
    |   |         |── data_analysis
    |   |         |
    |   |         |── data_visualization
    |   |         |
    |   |         |── helper_functions
    |   |
    |   ├── data_quality_tests      <- Contains data quality tests that test raw, processed and intermediary datasets.
    |                        
    |
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    |
    |
    |── environment.yml    <- A .yml file for reproducing the analysis environment.
    |
    │
    |── dodo.py            <- A file that contains all the information needed to run automation package Doit. Used to implement DAG structure.
    |
    |
    |── setup.py           <- A file that contains information about the packaging of the code.
    |
    |
    |── .gitignore         <- A file to specify which folders/files will be flagged with gitignore
    |
    |
```
--------

## References ##

**PUT REFERENCES HERE**

