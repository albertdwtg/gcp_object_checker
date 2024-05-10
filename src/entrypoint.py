import os

from flask import Flask
from main import run
from flask import request
import json
from threading import Thread
import main

container_port = os.environ.get("CONTAINER_PORT")

app = Flask(__name__)

@app.route("/", methods=['POST'])
def entrypoint():
    
    envelope = request.get_json()
    if not envelope:
        msg = "no Pub/Sub message received"
        return f"Bad Request: {msg}", 400

    if not isinstance(envelope, dict) or "message" not in envelope:
        msg = "invalid Pub/Sub message format"
        return f"Bad Request: {msg}", 400
    
    # data_args = read_pubsub_message(envelope = envelope)
    Thread(target=read_pubsub_message, args = [envelope]).start()
    #-- Execute function code
    # run(**data_args)
    return "OK"


def load_env_variables(input_variables: dict) -> None:
    """Function that read input variables coming from request
    and load them into envrionment variables

    Args:
        input_variables (dict): varaibles to load in environment variables
    """
    for k, v in input_variables.items():
        os.environ[k] = v
        
def read_pubsub_message(envelope: dict) -> dict:
    import base64
    import ast 
     
    pubsub_message = envelope["message"]
    data_args = {}
    if isinstance(pubsub_message, dict) and "data" in pubsub_message:
        data = base64.b64decode(pubsub_message["data"]).decode("utf-8").strip()
        # data_args = json.loads(data)
        data_args = ast.literal_eval(data)
    main.run(**data_args)
    return data_args

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=container_port)