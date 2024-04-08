#!/usr/bin/python3
"""
module taht start Flask web applcation
"""
from flask import Flask


app = Flask(__name__)

app.route("/", strict_slashes=False)
def hello_HBNB():
    """
    This method display an string
    """
    return "Hello HBNB!"
