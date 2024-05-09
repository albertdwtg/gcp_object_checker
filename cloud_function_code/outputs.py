from dataclasses import dataclass, field
import uuid
import requests
import google.oauth2.id_token
import google.auth.transport.requests

@dataclass(kw_only = True)
class Execution:
    job_name: str
    job_id: str
    execution_id: str = field(init=False)
    request_url: str
    request_params: dict
    
    def __post_init__(self):
        self._create_execution_id()
        pass
    
    def _create_execution_id(self):
        self.execution_id = uuid.uuid4().hex
    
    def run_request(self):

        request = google.auth.transport.requests.Request()
        audience = self.request_url

        id_token = google.oauth2.id_token.fetch_id_token(request, audience)
        # headers = {'Authorization': f'bearer {id_token}'}
        # service_response = requests.get(audience, headers=headers)
        
        print("ID TOKEN : ", id_token)
        
        response = requests.post(
            headers = {'Authorization': f'bearer {id_token}'},
            url = self.request_url,
            data = self.request_params
        )
        
        print("RESPONSE: ", response)
        print("RESPONSE: ", response.status_code)
        print("RESPONSE: ", response.text)