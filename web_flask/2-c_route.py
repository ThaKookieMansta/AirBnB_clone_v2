#!/usr/bin/python3
"""
Starts a Flask web application listens on 0.0.0.0, port 5000.
"""
from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    """
    This function displays hello HBNB
    Returns:

    """
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """
    Displays 'HBNB'.
    Returns:

    """
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c(text):
    """
    Displays 'C' followed by the value of <text>.
    Args:
        text:

    Returns:

    """
    text = text.replace("_", " ")
    return "C {}".format(text)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
