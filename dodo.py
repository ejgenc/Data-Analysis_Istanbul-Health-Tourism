from pathlib import Path # To wrap around filepaths

def task_clear_data_output():
    action_path = Path("src/data_preparation/clear_data_output.py")
    return {
        "actions": ["python {}".format(action_path)]
    }

def task_clear_viz_output():
    action_path = Path("src/data_preparation/clear_viz_output.py")
    return {
        "actions": ["python {}".format(action_path)]
    }
    
def task_run_data_preparation_helper_functions_unit_tests():
    action_path = Path("tests/unit_tests/helper_functions/test_data_preparation_helper_functions.py")
    return {
        "actions": ["pytest {}".format(action_path)],
        "file_dep": [Path("src/helper_functions/data_preparation_helper_functions.py")],
    }

def task_run_data_analysis_helper_functions_unit_tests():
    action_path = Path("tests/unit_tests/helper_functions/test_data_analysis_helper_functions.py")
    return {
        "actions": ["pytest {}".format(action_path)],
        "file_dep": [Path("src/helper_functions/data_analysis_helper_functions.py")],
    }

def task_run_data_visualization_helper_functions_unit_tests():
    action_path = Path("tests/unit_tests/helper_functions/test_data_visualization_helper_functions.py")
    return {
        "actions": ["pytest {}".format(action_path)],
        "file_dep": [Path("src/helper_functions/data_visualization_helper_functions.py")],
    }

def task_process_airbnb_data():
    action_path = Path("src/data_preparation/process_airbnb_data.py")
    return {
        "file_dep": [Path("data/raw/istanbul_airbnb_raw.csv")],
        "actions": ["python {}".format(action_path)],
        "targets": [Path("data/processed/istanbul_airbnb_processed.csv")]
    }

def task_run_data_quality_tests_for_processed_airbnb_data():
    action_path = Path("tests/data_quality_tests/test_istanbul_airbnb_processed_data_quality.py")
    return {
        "file_dep": [Path("data/processed/istanbul_airbnb_processed.csv")],
        "task_dep": ["process_airbnb_data"],
        "actions": ["pytest {}".format(action_path)]
    }

def task_convert_airbnb_data_to_shapefile():
    action_path = Path("src/data_preparation/convert_airbnb_data_to_shapefile.py")
    return {
        "file_dep": [Path("data/processed/istanbul_airbnb_processed.csv"),
                    Path("data/processed/hair_clinics_processed.shp")],
        "task_dep": ["run_data_quality_tests_for_processed_airbnb_data"],
        "actions": ["python {}".format(action_path)]
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

def task_run_data_quality_tests_for_processed_htourism_centers_data():
    action_path = Path("tests/data_quality_tests/test_htourism_centers_processed_data_quality.py")
    return {
        "file_dep": [Path("data/processed/htourism_centers_processed.shp")],
        "task_dep": ["combine_aesthethic_clinic_hclinic_shapefiles"],
        "actions": ["pytest {}".format(action_path)]
    }

def task_run_nearest_neighbor_analysis():
    action_path = Path("src/data_analysis/nearest_neighbor_analysis.py")
    return {
        "file_dep": [Path("data/processed/htourism_centers_processed.shp"),
                    Path("data/processed/istanbul_airbnb_processed_shapefile.shp")],
        "task_dep": ["combine_aesthethic_clinic_hclinic_shapefiles",
                    "convert_airbnb_data_to_shapefile",
                    "run_data_quality_tests_for_processed_htourism_centers_data"],
        "actions": ["python {}".format(action_path)],
        "targets": [Path("data/final/nn_analysis_results_all.csv"),
                    Path("data/final/nn_analysis_results_norm_atasehir.csv"),
                    Path("data/final/nn_analysis_results_norm_besiktas.csv"),
                    Path("data/final/nn_analysis_results_norm_kadikoy.csv"),
                    Path("data/final/nn_analysis_results_norm_sisli.csv"),
                    Path("data/final/nn_analysis_results_norm_uskudar.csv"),
                    Path("data/final/nn_analysis_results_normalized.csv")]
    }

def task_process_nearest_neighbor_analysis_results():
    action_path = Path("src/data_preparation/process_nearest_neighbor_analysis_results.py")
    return {
        "file_dep": [Path("data/final/nn_analysis_results_all.csv"),
                     Path("data/processed/istanbul_airbnb_processed_shapefile.shp")],
        "task_dep": ["run_nearest_neighbor_analysis",
                     "convert_airbnb_data_to_shapefile"],
        "actions": ["python {}".format(action_path)],
        "targets": [Path("data/final/distance_price_dataset.shp")]
    }

def task_analyze_geographic_distribution_of_htourism_centers():
    action_path = Path("src/data_analysis/analyze_geographic_distribution_of_htourism_centers.py")
    return {
        "file_dep": [Path("data/processed/htourism_centers_processed.shp"),
                    Path("data/external/istanbul_districts.shp"),
                    Path("data/external/district_income.xlsx")],
        "task_dep": ["combine_aesthethic_clinic_hclinic_shapefiles"],
        "actions": ["python {}".format(action_path)],
        "targets": [Path("data/final/geographic_distribution_of_htourism_centers.shp")]
    }

def task_analyze_geographic_distribution_of_airbnb_rentals():
    action_path = Path("src/data_analysis/analyze_geographic_distribution_of_airbnb_rentals.py")
    return {
        "file_dep": [Path("data/processed/istanbul_airbnb_processed_shapefile.shp"),
                    Path("data/external/istanbul_districts.shp"),
                    Path("data/external/district_income.xlsx")],
        "task_dep": ["convert_airbnb_data_to_shapefile"],
        "actions": ["python {}".format(action_path)],
        "targets": [Path("data/final/geographic_distribution_of_airbnb_rentals.shp")]
    }

def task_visualize_geographic_distribution_of_htourism_centers():
    action_path = Path("src/data_visualization/visualize_geographic_distribution_of_htourism_centers.py")
    return {
        "file_dep": [Path("data/final/geographic_distribution_of_htourism_centers.shp"),
                    Path("data/processed/htourism_centers_processed.shp"),
                    Path("data/external/istanbul_districts.shp")],
        "task_dep": ["analyze_geographic_distribution_of_htourism_centers"],
        "actions": ["python {}".format(action_path)],
        "targets": [Path("media/figures/raw/visualize_geographic_distribution_of_htourism")]
    }

def task_visualize_bivariate_analysis_htourism_center_count_at_district_level():
    action_path = Path("src/data_visualization/visualize_bivariate_analysis_htourism_center_count_at_district_level.py")
    return {
        "file_dep": [Path("data/final/geographic_distribution_of_htourism_centers.shp")],
        "task_dep": ["analyze_geographic_distribution_of_htourism_centers"],
        "actions": ["python {}".format(action_path)],
        "targets": [Path("media/figures/raw/visualize_bivariate_analysis_htourism_center_count_at_district_level")]
    }

def task_visualize_geographic_distribution_of_airbnb_rentals():
    action_path = Path("src/data_visualization/visualize_geographic_distribution_airbnb_rentals.py")
    return {
        "file_dep": [Path("data/final/geographic_distribution_of_airbnb_rentals.shp"),
                    Path("data/processed/istanbul_airbnb_processed_shapefile.shp"),
                    Path("data/external/istanbul_districts.shp")],
        "task_dep": ["analyze_geographic_distribution_of_airbnb_rentals"],
        "actions": ["python {}".format(action_path)],
        "targets": [Path("media/figures/raw/visualize_geographic_distribution_airbnb")]
    }

def task_visualize_bivariate_analysis_airbnb_count_at_district_level():
    action_path = Path("src/data_visualization/visualize_bivariate_analysis_airbnb_count_at_district_level.py")
    return {
        "file_dep": [Path("data/final/geographic_distribution_of_airbnb_rentals.shp")],
        "task_dep": ["analyze_geographic_distribution_of_airbnb_rentals"],
        "actions": ["python {}".format(action_path)],
        "targets": [Path("media/figures/raw/visualize_bivariate_analysis_airbnb_count_at_district_level")],
    }

def task_visualize_price_distribution_of_airbnb_rentals_kdeplot():
    action_path = Path("src/data_visualization/visualize_price_distribution_of_airbnb_rentals_kdeplot.py")
    return {
        "file_dep": [Path("data/processed/istanbul_airbnb_processed.csv")],
        "task_dep": ["run_data_quality_tests_for_processed_airbnb_data"],
        "actions": ["python {}".format(action_path)],
        "targets": [Path("media/figures/raw/visualize_price_distribution_of_airbnb_rentals_kdeplot")]
    }

def task_visualize_nearest_neighbor_analysis_confirmation():
    action_path = Path("src/data_visualization/visualize_nearest_neighbor_analysis_confirmation.py")
    return {
        "file_dep": [Path("data/final/nn_analysis_results_all.csv"),
                    Path("data/final/nn_analysis_results_norm_atasehir.csv"),
                    Path("data/final/nn_analysis_results_norm_besiktas.csv"),
                    Path("data/final/nn_analysis_results_norm_kadikoy.csv"),
                    Path("data/final/nn_analysis_results_norm_sisli.csv"),
                    Path("data/final/nn_analysis_results_norm_uskudar.csv"),
                    Path("data/final/nn_analysis_results_normalized.csv")],
        "task_dep": ["run_nearest_neighbor_analysis"],
        "actions": ["python {}".format(action_path)],
        "targets": [Path("media/figures/raw/visualize_nearest_neighbor_analysis_confirmation")]
    }

def task_visualize_nearest_neighbor_analysis_correlation_results():
    action_path = Path("src/data_visualization/visualize_nearest_neighbor_analysis_correlation_results.py")
    return {
        "file_dep": [Path("data/final/distance_price_dataset.shp")],
        "task_dep": ["process_nearest_neighbor_analysis_results"],
        "actions": ["python {}".format(action_path)],
        "targets": [Path("media/figures/raw/visualize_nearest_neighbor_analysis_correlation_results")]
    }