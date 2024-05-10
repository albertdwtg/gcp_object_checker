import uuid
from dataclasses import dataclass, field

import google.auth.transport.requests
import google.oauth2.id_token
import requests
from google.cloud import pubsub_v1
publisher = pubsub_v1.PublisherClient()


@dataclass(kw_only=True)
class Execution:
    """Class to represent execution objects
    """
    job_name: str
    job_id: str
    execution_id: str = field(init=False)
    request_url: str
    request_params: dict

    def __post_init__(self):
        # -- create a unique ID for each execution
        self.execution_id = uuid.uuid4().hex

    def run_request(self):
        # # -- get token to invoke cloud run
        # request = google.auth.transport.requests.Request()
        # id_token = google.oauth2.id_token.fetch_id_token(
        #     request, 
        #     self.request_url
        # )

        # # -- Post request with required params
        # response = requests.post(
        #     headers={'Authorization': f'bearer {id_token}'},
        #     url=self.request_url,
        #     json=self.request_params
        # )
        
        data = str(self.request_params).encode("utf-8")
        publisher.publish(
            self.request_url,
            data
        )
        print("Published")
