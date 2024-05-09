import os

from flask import Flask
from main import run
from flask import request
import json

container_port = os.environ.get("CONTAINER_PORT")

app = Flask(__name__)

@app.route("/", methods=['POST'])
def entrypoint():
    name = os.environ.get("NAME", "World")
    print(request.data)
    input_variables = request.data.decode()
    input_variables = json.loads(input_variables)
    load_env_variables(input_variables = input_variables)
    print(run())
    return f"Hello {name}!"


def load_env_variables(input_variables: dict) -> None:
    for k, v in input_variables.items():
        os.environ[k] = v

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=container_port)