## login page

from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "sqlite:////Users/SAMSUNG/Desktop/enochk/Python Programs/stock_tracker/database.db"
db = SQLAlchemy(app)


class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))


@app.route("/")
def login_prompt():
    return render_template("login.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # if no username and/or no password, then return error message
        # if username is not in db, then return error message

        uname = request.form["username"]
        passw = request.form["password"]

        login = user.query.filter_by(username=uname, password=passw).first()
        import pdb

        pdb.set_trace()
        if login is not None:
            return render_template("to_be_created.html")
            # return redirect(url_for("login_prompt"))
    return render_template("login.html")


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/create_account", methods=["GET", "POST"])
def create_account():
    if request.method == "POST":
        uname = request.form["reg_username"]
        passw = request.form["reg_password"]
        retype_passw = request.form["reg_retype_password"]

        new_account = user(username=uname, password=passw)
        db.session.add(new_account)
        db.session.commit()

    return render_template("login.html")


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)