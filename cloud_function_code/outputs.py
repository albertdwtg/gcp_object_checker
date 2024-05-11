import uuid
from typing import List
from dataclasses import dataclass, field
from google.cloud import pubsub_v1
publisher = pubsub_v1.PublisherClient()


@dataclass(kw_only=True)
class Execution:
    """Class to represent execution objects
    """
    job_name: str
    job_id: str
    execution_id: str = field(init=False)
    topic_path: str
    message_params: dict
    # depends_on: List[int] = field(init=False)
    done: bool = field(default=False, init=False)

    def __post_init__(self):
        # -- create a unique ID for each execution
        self.execution_id = uuid.uuid4().hex
        
    
    def send_message(self):
        """Function to send a message through pubsub with desired params
        """
        data = str(self.message_params).encode("utf-8")
        future = publisher.publish(
            self.topic_path,
            data
        )
        self.done = True
