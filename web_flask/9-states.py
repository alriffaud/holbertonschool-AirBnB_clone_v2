#!/usr/bin/python3
"""This script starts a Flask web application"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route("/states", strict_slashes=False)
def states_list():
    """This function display a HTML page (inside the tag BODY)"""
    states = storage.all(State).values()
    return (render_template("9-states.html", states=states))


@app.route("/states/<id>", strict_slashes=False)
def state_id(id=None):
    """This function display a HTML page (inside the tag BODY)"""
    states = storage.all(State).values()
    return (render_template("9-states.html", states=states, id=id))


@app.teardown_appcontext
def teardown(exception):
    """This function removes the current SQLAlchemy session"""
    storage.close()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
