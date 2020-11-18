# A Tribute to My Wrongness: How Health Tourism Interacts with Airbnb Rents in Istanbul #

![A sneak peek into the results of the analysis conducted in this project.](https://github.com/ejgenc/Data-Analysis_Istanbul-Health-Tourism/blob/master/media/figures/processed/visualize_nearest_neighbor_analysis_confirmation/confirmation_collage_eng.png)
_A sneak peek into the results of the analysis conducted in this project._

* * *

## External Links ##

The results of this analysis are offered as Medium articles. Be sure to check them out!

- [Medium Article (in English)](#)
- [Medium Article (in Turkish)](#)
 
## What is this project about? ##

Motivated by [my previous data analysis project](https://github.com/ejgenc/Data-Analysis_Istanbul-Health-Services-Map) about the distribution of health services across Istanbul, I have come up with another urban data analysis project. This time, **I am looking at various datasets to see whether there is some kind of a linear or monotonic relationship in between the price of an Airbnb rental and its closeness to a health tourism institution.**

## Technical Details ##

This Python project features a few major technical improvements over the last one. **I've organized the whole analysis with reproducibility in mind.**
To ensure succesful replication, I've created a minimal packaging of the project, the environment and the steps that are needed to reproduce the analysis.
The following Python packages were used to ensure replicability:

* [**doit**](https://pydoit.org/) --> A Python build tool like _Make_ that is used to order all the scripts in a pipeline fashion.
* [**pytest**](https://docs.pytest.org/en/stable/) --> Used in unit testing helper functions and doing data quality testing on intermediate datasets.

The geospatial analysis portion of the project is done with the help of the following packages:

* [**GeoPandas**](https://geopandas.org/) --> Pandas for geospatial data, supports metadata such as CRS.
* [**Shapely**](https://shapely.readthedocs.io/en/stable/manual.html) --> A Python package that handles geometric objects such as points and polygons.
* [**Geopy**](https://geopy.readthedocs.io/en/stable/) --> A Python package for GIS operations such as geocoding and distance calculation.
* [**Contextily**](https://github.com/geopandas/contextily) --> A Python package that provides basemap functionality.

Packages such as **Selenium, Numpy, Pandas, Matplotlib and Seaborn** were also used in the scraping, the processing, the analysis and the visualization of the data.

* * *

## How to reproduce this analysis? ##

### Why reproducibility? ###

I believe that openness and ease of reproduction are two very important concepts that build a foundation of trust under the dissemination of knowledge. You can always consume only the end result of my project by reading my Medium articles. However, there may be people who may want to be able to re-create my analysis steps one by one. This is the reason why this project was built with reproducibility in mind.

### How to reproduce this project? ###

Successful reproduction of a data science/analysis project requires the communication of the information that is related to the reproduction of the environment that the project was conducted in first. Only then can the analysis be replicated succesfully.  

#### 1.) Clone or download the project files

Before creating the environment, you need to have the project files on your computer. **You can download the source code of this project and the related material either through cloning the repository using a Git client, using GitHub desktop or through manual download.**

#### 2.) Recreate the environment that the analysis was conducted in ####

I decided to use [**Conda package manager**](https://docs.conda.io/en/latest/) as a package and environment manager for this project. **This was the preferred method of environment replication for this project because the conda package manager is more likely to download the main dependencies and their co-dependencies is a way that fits your specific operation system.**

##### Using the environment.yml file with Conda package manager #####

First, CD to the root of the project directory that you have downloaded. Then run the following command in the Anaconda prompt (or any terminal where you can run conda package manager from from):

`conda env create -f environment.yml`

Running this command will make conda create a new environment similar to the environment of the analysis with the information provided inside the **environment.yml** file. "healthtourism" will be name of this new environment. **The specific Python version that the analysis was conducted in is also encoded into the environment.yml file.**

Once you are done, **don't forget to activate your environment before running the analysis.** You can activate the environment using the following command:

`conda activate healthtourismenv`

#### 3.) Utilize the Python doit package to replicate the analysis ####

[The doit package](https://pydoit.org/) is a handy tool in Python that can be used to automate certain tasks, including data analysis workflows. This project makes use of the doit package to make replication easier. All the information related to the pipeline structure of the analysis is located in the **dodo.py** file.

To run the whole cleaning, analysis and visualization process from start to finish, do the following:

* Open a Python interpreter or any command line tool you can run Python from

* Activate the environment you have created in the previous step

* cd to the root project folder, the folder in which the **dodo.py** file is located.

* Simply run the following commands in the following order: `doit forget` and then `doit`

Whenever you want to re-run the analysis, repeat the two commands in the same order.

**Attention!** Running the whole pipeline on your computer skips two parts of the original analysis:

* Scraping the web for a part of the "hair transplant clinics" datasets. **This part is skipped on purpose to prevent the analysis from being corrupted due to a subsequent change in the websites scraped.** Still, the raw scraped dataset it provided with the source code.

* Manual editing of the final data visualizations. **The data visualizations used in the report were manually edited and translated to Turkish.** However, these changes are not major and you can verify the differences because the "raw" data visualizations will still be re-created.

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
    |
    |── media              <- Contains internally generated figures and external photos. Internally generated figures come with a license.
    |    ├── external_media <- Images and media downloaded from third party resources. A .txt file of references and attribution is included.
    │    ├── figures        <- Data visualizations generated through scripts.
    |                                             
    |
    ├── references         <- Data dictionaries, manuals, and all other explanatory material.
    │
    |
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    |
    |
    ├── self_documentation <- Certain notes that the author has written for himself. These files were not created with external viewers in mind.
    |
    |
    ├── src                         <- Source code used in this project.
    │   │
    │   ├── data_preparation        <- Scripts to download or generate data.
    │   |
    |   |── data_analysis           <- Scripts to generate intermediary datasets to base visualizations on.                           
    |   |   
    │   |── data_visualization      <- Scripts to create visualizations.
    |   |
    |   |── helper_functions        <- Scripts that contain various helper functions.
    |   
    │       
    ├── tests                       <- Contains test modules that test the data analysis pipeline.
    |   |
    |   ├── unit_tests              <- Contains unit tests. Folder structure mirrors that of the folder src.
    |   |         |
    |   |         |
    |   |         |── helper_functions
    |   |
    |   ├── data_quality_tests      <- Contains data quality tests for some of the datasets.
    |                        
    |
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         Generated with `pip freeze > requirements.txt`
    |
    |
    |── environment.yml    <- A .yml file for reproducing the analysis environment.
    |                         Generated with "conda env export --from-history -f environment.yml"
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

**A comprehensive reference of all the external sources and acknowledgements can be found under** `"references/references.txt"`
However, here is a brief mention of crucial dataset sources and acknowledgements:

### Dataset Sources for Raw Data ###

#### hair_clinics_raw.csv ####

A dataset that contains name and coordinate information for hair transplant clinics in Istanbul. Scraped from [this website](https://www.sacekimiburada.com/istanbul-sac-ekim-merkezleri") using the script located at `../src/data_preparation/scrape_web_for_hclinics.py`

#### istanbul_airbnb_raw.csv ####

A dataset that contains the data related to Airbnb rentals in Istanbul. Contains information such as location and price. Taken from a project called [_Inside Airbnb._](http://insideairbnb.com/) Data belongs to May 2019. Accessed through [this link to the data repository.](http://insideairbnb.com/get-the-data.html)

#### istanbul_healthservices_raw.csv ####

A dataset that contains information about all the health service providers in Istanbul. Downloaded from Istanbul Metropolitan Municipality's [Open Data Portal](https://data.ibb.gov.tr/en/). Accessed through [this link to the dataset.](https://data.ibb.gov.tr/dataset/istanbul-saglik-kurum-ve-kuruluslari-verisi)

### Acknowledgements ###

The geospatial processing part of the analysis was heavily inspired by the 2019 edition of the course called ["Automating GIS Processes".](https://automating-gis-processes.github.io/site/) The course was created for the University of Helsinki by Henrikki Tenkanen and Vuokko Heikinheimo.

The project structure was heavily inspired by Driven Data's [Cookiecutter Data Science project structure.](https://drivendata.github.io/cookiecutter-data-science/)



