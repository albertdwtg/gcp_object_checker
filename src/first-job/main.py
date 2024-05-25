import time
from open_weather import Client

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
        dataset_id = "open_weather_raw_data",
        partition_field = ""
    )
    print("image run 1")