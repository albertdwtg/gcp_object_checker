import os

from flask import Flask
from main import run
from flask import request
import json

container_port = os.environ.get("CONTAINER_PORT")

app = Flask(__name__)

@app.route("/", methods=['POST'])
def entrypoint():
    print(request.data)
    #-- Load input variables
    input_variables = request.data.decode()
    input_variables = json.loads(input_variables)
    load_env_variables(input_variables = input_variables)
    
    #-- Execute function code
    run()
    return "OK"


def load_env_variables(input_variables: dict) -> None:
    """Function that read input variables coming from request
    and load them into envrionment variables

    Args:
        input_variables (dict): varaibles to load in environment variables
    """
    for k, v in input_variables.items():
        os.environ[k] = v

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=container_port)