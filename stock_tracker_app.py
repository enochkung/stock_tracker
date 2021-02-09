## stock tracker

from flask import Flask, request, render_template, redirect, url_for
from typing import Dict
import yfinance as yf

app = Flask(__name__)

monitored_stock: Dict[str, Dict[str, float]] = dict()
labels = ["today's opening price: ", "today's high:", "today's low:"]


def obtain_stock_info(stock):
    quote = yf.Ticker(stock)
    period = "10d"
    interval = "1d"
    hist = quote.history(period=period, interval=interval)

    hist = hist.sort_index(ascending=False)
    current_open = hist["Open"][0]
    current_high = hist["High"][0]
    current_low = hist["Low"][0]

    return [current_open, current_high, current_low]


@app.route("/")
# @app.route("/home")
def display_home():
    return render_template("tracker_homepage.html")
    # return render_template("example_menu.html")


@app.route("/to_be_created", methods=["POST"])
def display_to_be_created():
    q1 = request.form["q1"]
    investments.append(0)
    return render_template("to_be_created.html")


@app.route("/stock_info", methods=["POST"])
def display_stock_info():
    stock = request.form["stock"]
    import pdb

    pdb.set_trace()
    if stock == "":
        stock = "HSBC"
    try:
        return redirect(url_for("find_stock_info", stock=stock))
    except KeyError:
        return render_template("to_be_created.html")


@app.route("/stock_info/<stock>")
def find_stock_info(stock):
    labels = ["today's opening price: ", "today's high:", "today's low:"]
    info = obtain_stock_info(stock)
    return render_template(
        "get_info_page.html",
        stock=stock,
        stats=info,
        labels=labels,
    )


@app.route("/monitor", methods=["POST"])
def display_monitor():
    stock = request.form["stock"]

    stock_info = obtain_stock_info(stock)
    monitored_stock[stock] = dict()
    for label_index, label in enumerate(labels):
        monitored_stock[stock][label] = stock_info[label_index]

    return render_template("monitored_info_page.html", stocks=monitored_stock)


if __name__ == "__main__":
    app.run(debug=True)