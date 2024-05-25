import time
from open_weather import Client

cities = {
    "Paris" : [48.853, 2.349],
    "Lisbon" : [38.717, -9.133],
    "Hong_kong" : [22.285, 114.158],
    "Beijing": [39.907, 116.397],
    "Shanghai": [31.222, 121.458]
}

def run(**kwargs):
    print(kwargs)
    c = Client("b964662692dfe4505387dd88765771bf")
    c.run_report(
        report_type="Daily",
        latitude=50,
        longitude=50,
        start_time = "2023-09-13",
        end_time = "2023-09-14",
        table_name = "test",
        project_id = "model-zoo-382809",
        dataset_id = "raw_data_air_quality",
        partition_field = ""
    )
    print("image run 1")
    
