import os

from flask import Flask
from main import run

app = Flask(__name__)

@app.route("/")
def hello_world():
    """Example Hello World route."""
    name = os.environ.get("NAME", "World")
    print(run())
    return f"Hello {name}!"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)