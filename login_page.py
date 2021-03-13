## login page

from flask import Flask, request, render_template, redirect, url_for, jsonify

import flask_sqlalchemy

app = Flask(__name__)


@app.route("/")
def login():
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)