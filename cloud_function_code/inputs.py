import hashlib
import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Tuple
import numpy as np

from outputs import Execution

topic_paths = json.loads(os.environ.get("TOPIC_PATHS"))

def range_of_dates(date_min: str, date_max: str, increment_day: int) -> List[str]:
    """Function used to generate a range of dates

    Args:
        date_min (str): start date of the range, in format YYYY-MM-DD
        date_max (str): end date of the range, in format YYYY-MM-DD
        increment_day (int): day to add between each date

    Raises:
        ValueError: If date_min >= date_max

    Returns:
        List[str]: range of dates in format YYYY-MM-DD
    """
    all_dates = []
    parsed_date_min = datetime.strptime(date_min, "%Y-%m-%d")
    parsed_date_max = datetime.strptime(date_max, "%Y-%m-%d")
    if(parsed_date_min>=parsed_date_max):
        raise ValueError("DATE_MIN must be lower than DATE_MAX")
    all_dates.append(parsed_date_min.strftime("%Y-%m-%d"))
    while parsed_date_min < parsed_date_max:
        parsed_date_min = parsed_date_min + timedelta(days = increment_day)
        all_dates.append(parsed_date_min.strftime("%Y-%m-%d"))
    return all_dates


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
    target_cloud_run: str = field(init=False)

    def __post_init__(self):
        self.__define_target_cloud_run()
        
        # -- create a job ID with a specific format
        self.job_id = self._create_job_id()

        # -- create executions for a Job
        self.job_executions_ids, self.job_executions = self._create_executions()
        self._validate_executions()

    def __define_target_cloud_run(self):
        if self.job_type in ["UNIQUE", "MULTIPLE"]:
            self.target_cloud_run = self.job_payload.get("target_cloud_run")
            if self.target_cloud_run is None:
                raise ValueError("You must define a value for target_cloud_run parameter")
    
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
                    topic_path=topic_paths[self.target_cloud_run],
                    message_params=self.job_payload.get("variables")
                )

                # -- append required infos to lists
                all_executions.append(execution_instance)
                all_executions_ids.append(execution_instance.execution_id)
            else:
                raise Exception(
                    "No topic paths provided in environment variables")
        if self.job_type == "MULTIPLE":
            all_executions_ids, all_executions = self.__create_executions_for_multiple_type()
        
        return all_executions_ids, all_executions

    def _validate_executions(self):
        """Function that checks if executions have been created

        Raises:
            ValueError: If no executions have been created
        """
        if len(self.job_executions) == 0 or len(self.job_executions_ids) == 0:
            raise ValueError("List of executions cannot be empty")

    def get_execution(self, execution_id: str) -> Execution:
        """Function used to get a specific execution based on its ID

        Args:
            execution_id (str): ID of the desired Execution 

        Returns:
            Execution: Execution desired, None if not found
        """
        instance = None
        for exec in self.job_executions:
            if exec.execution_id == execution_id:
                instance = exec
        return instance
    
    def __create_executions_for_multiple_type(self):
        all_executions = []
        all_executions_ids = []
        if "variables" not in self.job_payload:
            variables_dict = {}
        else:
            variables_dict = self.job_payload["variables"].copy()
        parallel_param = self.job_payload.get("parallel_param")
        parallel_type = self.job_payload.get("parallel_type")
        if parallel_type == "NUMERIC":
            parallel_min = self.job_payload.get("parallel_min")
            parallel_max = self.job_payload.get("parallel_max")
            parallel_step = self.job_payload.get("parallel_increment")
            array = np.arange(parallel_min, parallel_max, parallel_step).tolist()
            for value in array:
                variables_dict[parallel_param] = value
                message_params = variables_dict.copy()
                execution_instance = Execution(
                    job_name=self.job_name,
                    job_id=self.job_id,
                    topic_path=topic_paths[self.target_cloud_run],
                    message_params=message_params
                )
                # -- append required infos to lists
                all_executions.append(execution_instance)
                all_executions_ids.append(execution_instance.execution_id)
        if parallel_type == "LIST":
            parallel_list = self.job_payload.get("parallel_list")
            for value in parallel_list:
                variables_dict[parallel_param] = value
                message_params = variables_dict.copy()
                execution_instance = Execution(
                    job_name=self.job_name,
                    job_id=self.job_id,
                    topic_path=topic_paths[self.target_cloud_run],
                    message_params=message_params
                )
                # -- append required infos to lists
                all_executions.append(execution_instance)
                all_executions_ids.append(execution_instance.execution_id)
        if parallel_type == "DATE":
            parallel_min = self.job_payload.get("parallel_min_date")
            parallel_max = self.job_payload.get("parallel_max_date")
            parallel_step = int(self.job_payload.get("parallel_increment_day"))
            range_of_dates = JobHandler.range_of_dates(
                date_min = parallel_min, 
                date_max = parallel_max,
                increment_day = parallel_step
            )
            for value in range_of_dates:
                variables_dict[parallel_param] = value
                message_params = variables_dict.copy()
                execution_instance = Execution(
                    job_name=self.job_name,
                    job_id=self.job_id,
                    topic_path=topic_paths[self.target_cloud_run],
                    message_params=message_params
                )
                # -- append required infos to lists
                all_executions.append(execution_instance)
                all_executions_ids.append(execution_instance.execution_id)
        return all_executions_ids, all_executions
                
            
    def run_executions(self):
        """Function that runs all executions of the Job
        """
        for exec in self.job_executions:
            exec.send_message()
            
    @classmethod
    def range_of_dates(cls, date_min: str, date_max: str, increment_day: int) -> List[str]:
        """Function used to generate a range of dates

        Args:
            date_min (str): start date of the range, in format YYYY-MM-DD
            date_max (str): end date of the range, in format YYYY-MM-DD
            increment_day (int): day to add between each date

        Raises:
            ValueError: If date_min >= date_max

        Returns:
            List[str]: range of dates in format YYYY-MM-DD
        """
        all_dates = []
        parsed_date_min = datetime.strptime(date_min, "%Y-%m-%d")
        parsed_date_max = datetime.strptime(date_max, "%Y-%m-%d")
        if(parsed_date_min>=parsed_date_max):
            raise ValueError("DATE_MIN must be lower than DATE_MAX")
        all_dates.append(parsed_date_min.strftime("%Y-%m-%d"))
        while parsed_date_min < parsed_date_max:
            parsed_date_min = parsed_date_min + timedelta(days = increment_day)
            all_dates.append(parsed_date_min.strftime("%Y-%m-%d"))
        return all_dates
