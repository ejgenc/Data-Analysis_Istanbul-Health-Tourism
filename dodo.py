from pathlib import Path # To wrap around filepaths

def task_run_data_preparation_helper_functions_unit_tests():
    action_path = Path("tests/unit_tests/helper_functions/test_data_preparation_helper_functions.py")
    return {
        "actions": ["pytest {}".format(action_path)]
    }

def task_process_airbnb_data():
    action_path = Path("src/data_preparation/process_airbnb_data.py")
    return {
        "file_dep": [Path("data/raw/istanbul_airbnb_raw.csv")],
        "actions": ["python {}".format(action_path)],
        "targets": [Path("data/processed/istanbul_airbnb_processed.csv")]
    }

def task_process_health_services_data():
    action_path = Path("src/data_preparation/process_health_services_data.py")
    return {
        "file_dep": [Path("data/raw/istanbul_healthservices_raw.csv")],
        "actions": ["python {}".format(action_path)],
        "targets": [Path("data/processed/istanbul_aesthethic_centers_processed.csv")]
    }

def task_convert_aesthetic_clinic_to_shapefile():
    action_path = Path("src/data_preparation/convert_aesthethic_clinic_to_shapefile.py")
    return {
        "file_dep": [Path("data/processed/istanbul_aesthethic_centers_processed.csv"),
                    Path("data/processed/hair_clinics_processed.shp")],
        "actions": ["python {}".format(action_path)],
        "targets": [Path("data/processed/istanbul_aesthethic_centers_processed_shapefile.shp")]
    }

# # # def task_scrape_web_for_hclinics():
# # #     action_path = Path("src/data_preparation/scrape_web_for_hclinics.py")
# # #     return {
# # #         "actions": ["python {}".format(action_path)],
# # #         "targets": [Path("data/raw/hair_clinics_raw.csv")]
# # #     }

def task_convert_hclinic_coords_to_points():
    action_path = Path("src/data_preparation/convert_hclinic_coords_to_points.py")
    return {
        "file_dep": [Path("data/raw/hair_clinics_raw.csv")],
        "actions": ["python {}".format(action_path)],
        "targets": [Path("data/processed/hair_clinics_processed.shp")]
    }

def task_combine_aesthethic_clinic_hclinic_shapefiles():
    action_path = Path("src/data_preparation/combine_aesthethic_clinic_hclinic_shapefiles.py")
    return {
        "file_dep": [Path("data/processed/hair_clinics_processed.shp"),
                    Path("data/processed/istanbul_aesthethic_centers_processed_shapefile.shp")],
        "actions": ["python {}".format(action_path)],
        "targets": [Path("data/processed/htourism_centers_processed.shp")]
    }