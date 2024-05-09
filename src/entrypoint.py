import os

from flask import Flask
from main import run
from flask import request

container_port = os.environ.get("CONTAINER_PORT")

app = Flask(__name__)

@app.route("/", methods=['POST'])
def hello_world():
    """Example Hello World route."""
    name = os.environ.get("NAME", "World")
    print(request.data)
    print(run())
    return f"Hello {name}!"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=container_port)