#!/usr/bin/python3
"""This script starts a Flask web application"""
from flask import Flask, render_template
from werkzeug.utils import escape

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """This function display 'Hello HBNB!' in '/'"""
    return ("Hello HBNB!")


@app.route("/hbnb", strict_slashes=False)
def hbnb_hbnb():
    """This function display “HBNB” in '/hbnb'"""
    return ("HBNB")


@app.route("/c/<text>", strict_slashes=False)
def hbnb_c(text):
    """This function display a text in '/c/<text>'"""
    text = escape(text).replace('_', ' ')
    return ("C {}".format(text))


@app.route("/python/<text>", strict_slashes=False)
@app.route("/python/", defaults={"text": "is cool"}, strict_slashes=False)
def hbnb_python(text):
    """This function display a text in '/python/<text>' or '/python/'"""
    text = escape(text).replace('_', ' ')
    return ("Python {}".format(text))


@app.route("/number/<int:n>", strict_slashes=False)
def hbnb_number(n):
    """This function display a text in '/number/<int:n>'"""
    return ("{} is a number".format(n))


@app.route("/number_template/<int:n>", strict_slashes=False)
def number_template(n):
    """This function display a HTML page only if n is an integer"""
    if isinstance(n, int):
        return (render_template("5-number.html", number=n))
    else:
        return ("Not found", 404)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
