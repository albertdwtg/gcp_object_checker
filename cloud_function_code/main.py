import json
from datetime import datetime, timezone
from jsonschema import validate

import functions_framework
from inputs import JobHandler, topic_paths


@functions_framework.http
def run(request):
    """Entrypoint of the Cloud Function. Will parse input request 
    and create Job and Executions asked

    Args:
        request (Request): request coming from Cloud Scheduler

    Returns:
        str: response
    """
    #-- convert input body into dictionnary
    payload = convert_payload_to_dict(request.data)
    try:
        validate_payload_schema(payload = payload)
    except Exception as e:
        raise ValueError(f"Your JSON payload is not valid : {str(e)}")
    
    #-- collect metadata from headers
    scheduler_name = request.headers.get("X-Cloudscheduler-Jobname")
    function_execution_id = request.headers.get("Function-Execution-Id")
    
    #-- create a JobHandler object
    my_job = JobHandler(
        job_name=scheduler_name,
        job_reception_time=current_utc_datetime(),
        job_payload=payload,
        job_type=payload["job_type"].upper(),
        job_creation_date=payload["creation_date"],
        job_owner=payload["job_owner"],
        function_execution_id=function_execution_id
    )
    print(my_job)

    #-- run executions of the JobHandler object
    my_job.run_executions()

    return "OK"


def convert_payload_to_dict(payload: bytes) -> dict:
    """Function that reads a JSON in bytes format coming from
    Cloud Scheduler and converts it into a python dictionnary

    Args:
        payload (bytes): JSON bytes coming from Cloud Scheduler

    Raises:
        Exception: If input JSON is not valid

    Returns:
        dict: converted dictionnary
    """
    try:
        payload_str = payload.decode().strip('"')
        payload_str = payload_str.replace("\\n", "")
        payload_str = payload_str.replace("\\", "")
        payload_str = payload_str.replace(" ", "")
        payload_dict = json.loads(payload_str)
    except Exception as e:
        raise Exception(f"Error while parsing JSON payload : {str(e)}")
    return payload_dict


def current_utc_datetime() -> str:
    """Function that returns the actual UTC timestamp in string

    Returns:
        str: current UTC timestamp
    """
    value = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    return value

def validate_payload_schema(payload: dict):
    filename = "./payload_schema.json"
    with open(filename) as f_in:
        schema =  json.load(f_in)
        
    cloud_run_names = [k for k, v in topic_paths.items]
    schema["properties"]["target_cloud_run"]["enum"] = cloud_run_names
    validate(
        instance = payload,
        schema = schema
    )