import requests
from datetime import datetime, timezone, timedelta
from typing import List
from google.cloud import bigquery
from google.cloud.exceptions import NotFound
bq_client = bigquery.Client()
import json

schema_json = [
    {
        "name": "utc_timestamp",
        "type": "TIMESTAMP",
        "mode": "NULLABLE"
    },
    {
        "name": "latitude",
        "type": "FLOAT64",
        "mode": "NULLABLE"
    },
    {
        "name": "longitude",
        "type": "FLOAT64",
        "mode": "NULLABLE"
    },
    {
        "name": "air_quality_index",
        "type": "INT64",
        "mode": "NULLABLE"
    },
    {
        "name": "co",
        "type": "FLOAT64",
        "mode": "NULLABLE"
    },
    {
        "name": "no",
        "type": "FLOAT64",
        "mode": "NULLABLE"
    },
    {
        "name": "no2",
        "type": "FLOAT64",
        "mode": "NULLABLE"
    },
    {
        "name": "o3",
        "type": "FLOAT64",
        "mode": "NULLABLE"
    },
    {
        "name": "so2",
        "type": "FLOAT64",
        "mode": "NULLABLE"
    },
    {
        "name": "pm2_5",
        "type": "FLOAT64",
        "mode": "NULLABLE"
    },
    {
        "name": "pm10",
        "type": "FLOAT64",
        "mode": "NULLABLE"
    },
    {
        "name": "nh3",
        "type": "FLOAT64",
        "mode": "NULLABLE"
    }
]

class Client:
    
    partitioning_field: str = "utc_timestamp"
    
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
    
    def run_report(self, report_type: str, latitude: float, 
                   longitude: float, start_time_str: str, end_time_str: str,
                   project_id: str, dataset_id: str,
                   table_name: str):
        #-- work on dates
        self.__check_date_format(
            start_time = start_time_str,
            end_time = end_time_str,
            report_type = report_type
        )
        start_time = self.__convert_date_to_unix(start_time_str)
        end_time = self.__convert_date_to_unix(end_time_str)-1
        
        #-- format request with params
        request_str = "http://api.openweathermap.org/data/2.5/air_pollution/history?lat={lat}&lon={long}&start={start}&end={end}&appid={api_key}"
        request_str = request_str.format(
            lat = latitude,
            long = longitude,
            start = start_time,
            end = end_time,
            api_key = self.api_key
        )
        
        #-- run request and format output
        response = requests.get(request_str)
        output_records = self.__format_output(json_response = response.json())
        
        full_table_name = f'{project_id}.{dataset_id}.{table_name}'
        schema = [bigquery.SchemaField(field["name"], field["type"], mode=field["mode"]) for field in schema_json]
        #-- create table if not exists
        try:
            table = bq_client.get_table(full_table_name)
        except NotFound:
            table = bigquery.Table(full_table_name, schema=schema)
            table.time_partitioning = bigquery.TimePartitioning(
                type_=bigquery.TimePartitioningType.DAY,
                field=self.partitioning_field, 
                expiration_ms=1000*60*60*24*365*5
            )

            bq_client.create_table(table, exists_ok = True)
        
        self.__delete_old_data(
            full_table_name = full_table_name,
            start_date = start_time_str,
            end_date = end_time_str
        )
        job_config = bigquery.LoadJobConfig()
        job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
        job_config.schema = schema
        job = bq_client.load_table_from_json(output_records, table, job_config = job_config)
    
    def __delete_old_data(self,full_table_name: str, start_date: str, end_date: str):

        query = """
        DELETE
            {full_table_name}
        WHERE {partitioning_field} BETWEEN "{start_date}" and "{end_date}"
        """
        query = query.format(
            full_table_name = full_table_name,
            partitioning_field = self.partitioning_field,
            start_date = start_date,
            end_date = end_date
        )
        job = bq_client.query(query)
        result = job.result()
        
        
    
    def __convert_date_to_unix(self, date_str: str) -> int:
        """function that converts a string date in format YYYT-MM-DD to its
        UTC unix timestamp

        Args:
            date_str (str): string of the date in format YYYY-MM-DD

        Returns:
            int: unix timestamp
        """
        try:
            # Parse the input date string
            dt_object = datetime.strptime(date_str, '%Y-%m-%d')
            # Calculate the Unix timestamp (seconds since January 1, 1970)
            unix_timestamp = dt_object.replace(tzinfo=timezone.utc).timestamp()
            return int(unix_timestamp)
        except ValueError:
            return "Invalid date format. Please provide a valid date in the format 'YYYY-MM-DD'."
    
    def __check_date_format(self, start_time: str, end_time: str, report_type: str):
        """function that checks string dates format

        Args:
            start_time (str): string of the start date in format YYYY-MM-DD
            end_time (str): string of the end date in format YYYY-MM-DD
            report_type (str): type of the report

        Raises:
            ValueError: If dates are not valid
        """
        start_time = datetime.strptime(start_time, '%Y-%m-%d')
        end_time = datetime.strptime(end_time, '%Y-%m-%d')
        if start_time >= end_time:
            raise ValueError("start_time must be lower than end_time")
        elif report_type.upper()=="DAILY" and end_time > start_time + timedelta(days=1):
            raise ValueError("In Daily report, delays between dates must be one day")
    
    def __format_output(self, json_response: dict) -> List[dict]:
        """Function that converts request JSON output to a valid format to be 
        written into BigQuery

        Args:
            json_response (dict): JSON response of the request

        Returns:
            List[dict]: formatted output
        """
        lat = json_response["coord"]["lat"]
        long = json_response["coord"]["lon"]
        all_records = []
        for record in json_response["list"]:
            record_dict = {
                self.partitioning_field: record["dt"],
                "latitude": lat,
                "longitude": long,
                "air_quality_index": record["main"].get("aqi"),
                "co": record["components"].get("co"),
                "no": record["components"].get("no"),
                "no2": record["components"].get("no2"),
                "o3": record["components"].get("o3"),
                "so2": record["components"].get("so2"),
                "pm2_5": record["components"].get("pm2_5"),
                "pm10": record["components"].get("pm10"),
                "nh3": record["components"].get("nh3"),
            }
            all_records.append(record_dict)
        return all_records