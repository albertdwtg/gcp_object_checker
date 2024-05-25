import time
from open_weather import Client
from google.cloud import secretmanager
from datetime import datetime, timedelta


cities = {
    "Paris" : [48.853, 2.349],
    "Lisbon" : [38.717, -9.133],
    "Hong_kong" : [22.285, 114.158],
    "Beijing": [39.907, 116.397],
    "Shanghai": [31.222, 121.458],
    "Arcachon": [44.650, -1.167],
    "Rome": [41.895, 12.484],
    "Copenhagen": [55.676, 12.566]
}

def run(**kwargs):
    
    c = Client("b964662692dfe4505387dd88765771bf")
    
    report_type = kwargs.get("report_type")
    if report_type.upper()=="CATCHUP":
        start_time = kwargs["start_time"]
        end_time = kwargs["end_time"]
    else:
        report_type = "DAILY"
        start_time = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
        end_time = datetime.today().strftime('%Y-%m-%d')
    
    for city, coord in cities.items():
        print(city, start_time, end_time)
        c.run_report(
            report_type=report_type,
            latitude=coord[0],
            longitude=coord[1],
            start_time_str = start_time,
            end_time_str = end_time,
            table_name = city.lower(),
            project_id = kwargs["project_id"],
            dataset_id = kwargs["dataset_id"]
        )
    

def access_secret_version(project_id, secret_id, version_id="latest"):
    # Create the Secret Manager client.
    secret_client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    # Access the secret version.
    response = secret_client.access_secret_version(name=name)

    # Return the decoded payload.
    return response.payload.data.decode('UTF-8')
    
