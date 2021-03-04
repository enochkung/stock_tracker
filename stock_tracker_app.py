## stock tracker

from flask import Flask, request, render_template, redirect, url_for, jsonify
from typing import Dict
import yfinance as yf
import numpy as np
from multiprocessing import Value
from yahoo_fin import stock_info

app = Flask(__name__)

monitored_stock: Dict[str, Dict[str, float]] = dict()
labels = ["today's opening price: ", "today's high:", "today's low:"]
monitored_stock = ["AAPL", "HSBC"]
purchased_stock = dict()
monitor_stock_price_dict = dict()
num_stock_purchased_dict = {"AAPL": "0", "HSBC": "0"}
total_value_dict = dict()

rando = np.random.rand()

seconds = Value("i", 0)


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
        if new_stock not in monitored_stock:
            monitored_stock.append(new_stock)
        # get whether buy or sell, and if buy whether in shares or cost
        action = [
            key for key in request.form if key != "stock" and request.form[key] != ""
        ][0]
        if action == "num_shares":
            num_stock_purchased_dict[new_stock] = request.form[action]
        elif action == "cost_shares":
            pass
        elif action == "sell_shares":
            pass

    ## get current information of the stocks
    for key in monitored_stock:
        [current_open, current_price, current_high, current_low] = obtain_stock_info(
            key
        )
        monitor_stock_price_dict[key] = round(current_price, 4)

    return render_template(
        "monitor_and_purchase.html",
        mon_dict=monitor_stock_price_dict,
        shares_dict=num_stock_purchased_dict,
    )


@app.route("/update_monitor", methods=["POST"])
def update_monitor():
    # if "stock" in request.form:
    #     print(request.form)
    for key in monitored_stock:
        [current_open, current_price, current_high, current_low] = obtain_stock_info(
            key
        )
        monitor_stock_price_dict[key] = round(current_price, 4)
    return jsonify(
        "",
        render_template(
            "update_monitor_table.html",
            mon_dict=monitor_stock_price_dict,
            shares_dict=num_stock_purchased_dict,
        ),
    )


@app.route("/to_be_created")
def display_to_be_created():
    return render_template("to_be_created.html")


# @app.route("/live_data")
# def display_live_data():
#     return render_template("live_data.html", index=rando)

# @app.route("/monitor", methods=["POST"])
# def display_monitor():
#     """ NEED CHANGE: will take input and add to monitor stock dict and then run true_monitor """
#     stock = request.form["stock"]
#     stock_info = obtain_stock_info(stock)
#     monitored_stock[stock] = dict()
#     for label_index, label in enumerate(labels):
#         monitored_stock[stock][label] = stock_info[label_index]
#     # return render_template("sample_table.html", stock="AAPL")
#     return render_template("monitored_info_page.html", stocks=monitored_stock)


if __name__ == "__main__":
    app.run(debug=True)