from dataclasses import dataclass, field
from datetime import datetime
from outputs import Execution
from typing import List
import hashlib
from enum import Enum
import os
import json

cloud_run_urls = json.loads(os.environ.get("CLOUD_RUN_URLS"))
print("VALUE : ", cloud_run_urls)

class JobType(Enum):
    PIPELINE = ""
    MULTIPLE = ""
    UNIQUE = ""
    

@dataclass(kw_only = True)
class JobHandler:
    job_name: str
    job_reception_time: str
    job_payload: dict
    job_type: str
    job_creation_date: str
    job_owner: str
    job_id: str = field(init=False)
    job_executions: List[Execution] = field(init=False)
    job_executions_ids: List[str] = field(init=False)
    function_execution_id: str
    
    def __post_init__(self):
        self.job_id = self._create_job_id()
        self._validate_job_type()
        self._validate_job_owner()
        self._validate_creation_date()
        self.job_executions_ids, self.job_executions = self._create_executions()
    
    def _create_job_id(self):
        job_name_hash = hashlib.md5(self.job_name.encode()).hexdigest()[:8]
        
        timestamp = datetime.now()
        format = "%Y%m%d_%H%M%S"
        date_timestamp = timestamp.strftime(format)
        job_id = job_name_hash + "_" + date_timestamp
        return job_id
    
    def _validate_job_type(self):
        possible_values = [name for name, member in JobType.__members__.items()]
        if self.job_type not in possible_values:
            raise ValueError(f"job_type value is not valid, possible values : {possible_values}")

    def _validate_job_owner(self):
        if any(char.isdigit() for char in self.job_owner):
            raise ValueError("Impossible to have digits in job_owner variable")
        if len(self.job_owner)<2:
            raise ValueError("Job_owner length is too short")
    
    def _validate_creation_date(self):
        date_split = self.job_creation_date.split("-")
        if len(date_split)!=3:
            raise ValueError("Incorrect format for creation_date, must be YYYY-MM-DD")
        elif (len(date_split[0])!=4 or len(date_split[1])!=2 or len(date_split[2])!=2):
            raise ValueError("Incorrect format for creation_date, must be YYYY-MM-DD")
        
    def _create_executions(self):
        all_executions = []
        all_executions_ids = []
        if self.job_type == "UNIQUE":
            if cloud_run_urls is not None:
                url = cloud_run_urls[self.job_name]
                params = self.job_payload.get("variables")
                execution_instance = Execution(
                    job_name = self.job_name,
                    job_id = self.job_id,
                    request_url = url,
                    request_params = params
                )
                all_executions.append(execution_instance)
                all_executions_ids.append(execution_instance.execution_id)
            else:
                raise Exception("No cloud run urls provided in environment variables")
        return all_executions_ids, all_executions
    
    def run_executions(self):
        for exec in self.job_executions:
            exec.run_request()