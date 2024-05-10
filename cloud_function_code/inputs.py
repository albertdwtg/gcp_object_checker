import hashlib
import json
import os
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Tuple

from outputs import Execution

topic_paths = json.loads(os.environ.get("TOPIC_PATHS"))


class JobType(Enum):
    """
    Enumerator that lists all availables job types
    """
    PIPELINE = ""
    MULTIPLE = ""
    UNIQUE = ""


@dataclass(kw_only=True)
class JobHandler:
    """
    Class to create Job object based on inputs coming from Cloud Scheduler
    """
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
        # -- create a job ID with a specific format
        self.job_id = self._create_job_id()

        # -- make some checks about input variables
        self._validate_job_type()
        self._validate_job_owner()
        self._validate_creation_date()

        # -- create executions for a Job
        self.job_executions_ids, self.job_executions = self._create_executions()
        self._validate_executions()

    def _create_job_id(self) -> str:
        """Generate unique ID for a job based on the hash of job
        name and current timestamp

        Returns:
            str: job ID in format "hash_YYYYMMDD_HHMMSS"
        """
        # -- get first characters of hash
        job_name_hash = hashlib.md5(self.job_name.encode()).hexdigest()[:8]

        # -- format timestamp
        timestamp = datetime.now()
        format = "%Y%m%d_%H%M%S"
        date_timestamp = timestamp.strftime(format)
        job_id = job_name_hash + "_" + date_timestamp
        return job_id

    def _validate_job_type(self):
        """Function that checks if job type value is valid,
        based on JobType enumerator

        Raises:
            ValueError: if job type value not present in JobType enumerator
        """
        possible_values = [name for name,
                           member in JobType.__members__.items()]
        if self.job_type not in possible_values:
            raise ValueError(
                f"job_type value is not valid, possible values : {possible_values}")

    def _validate_job_owner(self):
        """Function that checks if job owner value is valid

        Raises:
            ValueError: If value contains a digit
            ValueError: If value is less than 2 characters
        """
        if any(char.isdigit() for char in self.job_owner):
            raise ValueError("Impossible to have digits in job_owner variable")
        if len(self.job_owner) < 2:
            raise ValueError("Job_owner length is too short")

    def _validate_creation_date(self):
        """Function that checks if creation date value is valid

        Raises:
            ValueError: if value is not is format YYYY-MM-DD
        """
        date_split = self.job_creation_date.split("-")
        if len(date_split) != 3:
            raise ValueError(
                "Incorrect format for creation_date, must be YYYY-MM-DD")
        elif (len(date_split[0]) != 4 or len(date_split[1]) != 2 or len(date_split[2]) != 2):
            raise ValueError(
                "Incorrect format for creation_date, must be YYYY-MM-DD")

    def _create_executions(self) -> Tuple[List[str], List[Execution]]:
        """Function that create all executions needed in the Job

        Raises:
            Exception: If cloud_run_urls value is empty

        Returns:
            Tuple[List[str], List[Execution]]: all ids of executions and all executions
        """
        # -- create lists that will be returned
        all_executions = []
        all_executions_ids = []

        # -- case when job type is UNIQUE
        if self.job_type == "UNIQUE":
            if topic_paths is not None:
                # -- create the only execution
                execution_instance = Execution(
                    job_name=self.job_name,
                    job_id=self.job_id,
                    topic_path=topic_paths[self.job_name],
                    message_params=self.job_payload.get("variables")
                )

                # -- append required infos to lists
                all_executions.append(execution_instance)
                all_executions_ids.append(execution_instance.execution_id)
            else:
                raise Exception(
                    "No cloud run urls provided in environment variables")
        return all_executions_ids, all_executions

    def _validate_executions(self):
        """Function that checks if executions have been created

        Raises:
            ValueError: If no executions have been created
        """
        if len(self.job_executions) == 0 or len(self.job_executions_ids) == 0:
            raise ValueError("List of executions cannot be empty")

    def run_executions(self):
        """Function that runs all executions of the Job
        """
        for exec in self.job_executions:
            exec.send_message()
