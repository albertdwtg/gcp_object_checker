import time
from open_weather import Client
from google.cloud import secretmanager


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
    # print(kwargs)
    
    c = Client("b964662692dfe4505387dd88765771bf")
    c.run_report(
        report_type="Daily",
        latitude=50,
        longitude=50,
        start_time = "2023-09-13",
        end_time = "2023-09-14",
        table_name = kwargs["table_name"],
        project_id = kwargs["project_id"],
        dataset_id = kwargs["dataset_id"]
    )
    print("image run 1")
    
def access_secret_version(project_id, secret_id, version_id="latest"):
    # Create the Secret Manager client.
    secret_client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    # Access the secret version.
    response = secret_client.access_secret_version(name=name)

    # Return the decoded payload.
    return response.payload.data.decode('UTF-8')
    
