import json
from datetime import datetime

import functions_framework
from inputs import JobHandler


@functions_framework.http
def run(request):
    payload = convert_payload_to_dict(request.data)
    scheduler_name = request.headers.get("X-Cloudscheduler-Jobname")
    function_execution_id = request.headers.get("Function-Execution-Id")
    my_job = JobHandler(
        job_name=scheduler_name,
        job_reception_time=current_utc_datetime,
        job_payload=payload,
        job_type=payload["job_type"].upper(),
        job_creation_date=payload["creation_date"],
        job_owner=payload["job_owner"],
        function_execution_id=function_execution_id
    )
    print(my_job)

    my_job.run_executions()

    return "OK"


def convert_payload_to_dict(payload: bytes):
    try:
        payload_str = payload.decode().strip('"')
        payload_str = payload_str.replace("\\n", "")
        payload_str = payload_str.replace("\\", "")
        payload_str = payload_str.replace(" ", "")
        payload_dict = json.loads(payload_str)
    except Exception as e:
        raise Exception(f"Error while parsing JSON payload : {str(e)}")
    return payload_dict


def current_utc_datetime():
    value = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    return value
