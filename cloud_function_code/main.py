import functions_framework
import json
from inputs import JobHandler

@functions_framework.http
def run(request):
    payload = convert_payload_to_dict(request.data)
    print(payload)
    print(request.headers)
    scheduler_name = request.headers.get("X-Cloudscheduler-Jobname")
    my_job = JobHandler(
        job_name = scheduler_name,
        job_reception_time = "2024",
        job_payload = payload,
        job_type = "UNIQUE"
    )
    print(my_job)
    
    return "OK"

def convert_payload_to_dict(payload: bytes):
    payload_str = payload.decode().strip('"')
    payload_dict = json.loads(payload_str)
    return payload_dict