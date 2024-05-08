from dataclasses import dataclass, field
from datetime import datetime
import hashlib
from enum import Enum

class JobType(Enum):
    PIPELINE = ""
    MULTIPLE = ""
    UNIQUE = ""
    
def validate_job_type(job_type: str):
    possible_values = [e.name for e in JobType]
    if job_type not in list(JobType.members):
        raise ValueError(f"job_type value is not valid, possible values : {possible_values}")
    return job_type
    

@dataclass(kw_only = True)
class JobHandler:
    job_name: str
    job_reception_time: str
    # job_start_date: str
    job_payload: dict
    job_type: str
    job_creation_date: str
    job_owner: str
    function_execution_id: str
    
    def __post_init__(self):
        self.job_id = self._create_job_id()
        validate_job_type(self.job_type)
    
    def _create_job_id(self):
        job_name_hash = hashlib.md5(self.job_name.encode()).hexdigest()[:8]
        
        timestamp = datetime.now()
        format = "%Y%m%d_%H%M%S"
        date_timestamp = timestamp.strftime(format)
        job_id = job_name_hash + "_" + date_timestamp
        return job_id