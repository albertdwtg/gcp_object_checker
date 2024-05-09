from dataclasses import dataclass, field
import uuid

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