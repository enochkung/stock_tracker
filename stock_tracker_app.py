## stock tracker

from flask import Flask, request, render_template, redirect, url_for, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, current_user, login_user, logout_user
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from typing import Dict
import yfinance as yf
import numpy as np
from multiprocessing import Value
from yahoo_fin import stock_info
from account_manage import test_login, UserModel, db, login
from monitor import monitor
from extras import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATA_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "secret_key"

db.init_app(app)

app.register_blueprint(login, url_prefix="/")
app.register_blueprint(monitor, url_prefix="/")
rando = np.random.rand()

seconds = Value("i", 0)


@app.before_first_request
def create_all():
    db.create_all()


@app.route("/")
@app.route("/home")
def display_home():
    # return render_template("login.html")
    return redirect(url_for("monitor.true_monitor"))


@app.route("/stock_info", methods=["POST"])
def display_stock_info():
    stock = request.form["stock"]
    if stock == "":
        stock = "HSBC"
    try:
        return redirect(url_for("find_stock_info", stock=stock))
    except KeyError:
        return render_template("to_be_created.html")


@app.route("/update_monitor", methods=["POST"])
def update_monitor():
    (
        monitor_stock_price_dict,
        total_value_dict,
        purchase_value_dict,
        value_color_dict,
    ) = get_current_price()

    update_top_level_portfolio()

    return jsonify(
        "",
        render_template(
            "update_monitor_table.html",
            top_level=top_level_info,
            mon_dict=monitor_stock_price_dict,
            shares_dict=num_stock_purchased_dict,
            purch_dict=purchase_value_dict,
            total_val_dict=total_value_dict,
            value_color_dict=value_color_dict,
        ),
    )


@app.route("/signup", methods=["POST", "GET"])
def signup():

    if current_user.is_authenticated:
        return redirect("/true_monitor")

    if request.method == "POST":
        username = request.form["reg_username"]
        password = request.form["reg_password"]
        re_password = request.form["reg_retype_password"]

        if password != re_password:
            return redirect("/signup")
        else:
            if UserModel.query.filter_by(username=username).first():
                return "Username taken"

        user = UserModel(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return render_template("login.html")

    return render_template("signup.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.form["username"] == "" or request.form["password"] == "":
        print("Please enter valid username and password!")
        return redirect((url_for("display_home")))
    else:
        # check whether username and password exists
        pass

    return redirect((url_for("display_to_be_created")))


@app.route("/to_be_created")
def display_to_be_created():
    return render_template("to_be_created.html")


if __name__ == "__main__":
    test_login.init_app(app)
    test_login.login_view = "account_manage.t_login"
    app.run(debug=True)