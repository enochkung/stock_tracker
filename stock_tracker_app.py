## stock tracker

from flask import Flask, request, render_template, redirect, url_for, jsonify
from typing import Dict
import yfinance as yf
import numpy as np
from multiprocessing import Value
from yahoo_fin import stock_info

app = Flask(__name__)


rando = np.random.rand()

seconds = Value("i", 0)


# global monitored_stock, labels, monitored_stock, purchased_stock, monitor_stock_price_dict, num_stock_purchased_dict, purchase_value_dict, purchase_value_dict, total_value_dict, value_color_dict, free_funds, invested, portfolio, returns
labels = ["today's opening price: ", "today's high:", "today's low:"]
monitored_stock = ["AAPL", "HSBC"]
purchased_stock = dict()
monitor_stock_price_dict = dict()
num_stock_purchased_dict = {"AAPL": 0, "HSBC": 0}
purchase_value_dict = {"AAPL": 0.0, "HSBC": 0.0}
total_value_dict = dict()
value_color_dict = dict()
top_level_info = {"free_funds": 0.0, "portfolio": 0.0, "invested": 0.0, "returns": 0.0}


def obtain_stock_info(stock):
    quote = yf.Ticker(stock)
    period = "10d"
    interval = "1d"
    hist = quote.history(period=period, interval=interval)

    hist = hist.sort_index(ascending=False)

    current_open = hist["Open"][0]
    current_price = stock_info.get_live_price(stock)
    current_high = hist["High"][0]
    current_low = hist["Low"][0]
    return [current_open, current_price, current_high, current_low]


@app.route("/")
@app.route("/home")
def display_home():
    # return render_template("tracker_homepage.html")
    return redirect(url_for("true_monitor"))


@app.route("/stock_info", methods=["POST"])
def display_stock_info():
    stock = request.form["stock"]
    if stock == "":
        stock = "HSBC"
    try:
        return redirect(url_for("find_stock_info", stock=stock))
    except KeyError:
        return render_template("to_be_created.html")


@app.route("/true_monitor", methods=["GET", "POST"])
def true_monitor():
    """ display monitor list and purchased list """

    ## if request.form contains bought stock
    if "stock" in request.form:
        # get stock abbrev.
        new_stock = request.form["stock"]
        # if stock is not already monitored, add to monitored stock list
        # num_stock_purchased_dict, purchase_value_dict = buy_or_sell_shares()
        buy_or_sell_shares(new_stock)

    elif "mon_stock" in request.form:
        ## if only add to monitor
        new_stock = request.form["mon_stock"]
        monitored_stock.append(new_stock)
        ## stock is not yet bought so set number of stock to zero
        num_stock_purchased_dict[new_stock] = 0

    elif "add_free_funds" in request.form:
        add_funds = request.form["add_free_funds"]
        top_level_info["free_funds"] += int(add_funds)

    ## get current information of the stocks
    (
        monitor_stock_price_dict,
        total_value_dict,
        purchase_value_dict,
        value_color_dict,
    ) = get_current_price()

    update_top_level_initial()

    return render_template(
        "monitor_and_purchase.html",
        top_level=top_level_info,
        mon_dict=monitor_stock_price_dict,
        shares_dict=num_stock_purchased_dict,
        purch_dict=purchase_value_dict,
        total_val_dict=total_value_dict,
        value_color_dict=value_color_dict,
    )


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


@app.route("/to_be_created")
def display_to_be_created():
    return render_template("to_be_created.html")


def set_colors(total_value, purchase_value):

    if total_value > np.round_(purchase_value, 2):
        return "green"
    elif total_value == np.round_(purchase_value, 2):
        return "grey"
    else:
        return "red"


def buy_or_sell_shares(new_stock):
    # if stock is not already monitored, add to monitored stock list
    if new_stock not in monitored_stock:
        monitored_stock.append(new_stock)
    # get whether buy or sell, and if buy whether in shares or cost
    action = [
        key for key in request.form if key != "stock" and request.form[key] != ""
    ][0]

    if action == "num_shares":
        # if action is in number of shares, then initiate stock in num_stock_purchased_dict at 0 stocks
        if new_stock not in num_stock_purchased_dict:
            num_stock_purchased_dict[new_stock] = 0
        # add the number of stocks to be purchased to already recorded number, whether 0 or non-0
        num_stock_purchased_dict[new_stock] += int(request.form[action])
    elif action == "cost_shares":
        # if action is in amount of shares by cost, then using current price, translate to number of shares
        shares_in_cost = float(request.form[action])
        stock_live_price = stock_info.get_live_price(new_stock)
        if new_stock not in num_stock_purchased_dict:
            num_stock_purchased_dict[new_stock] = 0
        # add the number of stocks to be purchased to already recorded number, whether 0 or non-0
        num_of_shares = shares_in_cost // stock_live_price
        num_stock_purchased_dict[new_stock] += int(shares_in_cost // stock_live_price)
    elif action == "sell_shares":
        # if action is sell number of shares, remove amount from num_stock_purchased_dict
        if new_stock in num_stock_purchased_dict:
            num_shares_sold = int(request.form[action])
            num_stock_purchased_dict[new_stock] = max(
                num_stock_purchased_dict[new_stock] - num_shares_sold, 0
            )

    purchase_value_dict[new_stock] = 0.0

    return num_stock_purchased_dict, purchase_value_dict


def get_current_price():
    for key in monitored_stock:
        [current_open, current_price, current_high, current_low] = obtain_stock_info(
            key
        )
        monitor_stock_price_dict[key] = np.round_(current_price, 2)
        total_value_dict[key] = np.round_(
            current_price * num_stock_purchased_dict[key], 2
        )
        if "stock" in request.form and request.form["stock"] == key:
            purchase_value_dict[key] += current_price * num_stock_purchased_dict[key]

        value_color_dict[key] = set_colors(
            total_value_dict[key], purchase_value_dict[key]
        )
    return (
        monitor_stock_price_dict,
        total_value_dict,
        purchase_value_dict,
        value_color_dict,
    )


def auto_buy_sell():
    pass


def update_top_level_initial():
    top_level_info["portfolio"] = sum(total_value_dict.values())
    if top_level_info["invested"] != 0:
        top_level_info["return"] = (
            str(
                round(
                    (top_level_info["portfolio"] - top_level_info["invested"])
                    / top_level_info["invested"]
                    * 100,
                    2,
                )
            )
            + "%"
        )
    else:
        top_level_info["return"] = "0%"

    top_level_info["invested"] = np.round_(sum(purchase_value_dict.values()), 2)
    top_level_info["free_funds"] -= top_level_info["invested"]


def update_top_level_portfolio():
    top_level_info["portfolio"] = sum(total_value_dict.values())
    if top_level_info["invested"] != 0:
        top_level_info["return"] = (
            str(
                round(
                    (top_level_info["portfolio"] - top_level_info["invested"])
                    / top_level_info["invested"]
                    * 100,
                    2,
                )
            )
            + "%"
        )
    else:
        top_level_info["return"] = "0%"


if __name__ == "__main__":
    app.run(debug=True)