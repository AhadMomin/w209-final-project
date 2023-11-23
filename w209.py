from flask import Flask, render_template
import altair as alt
import pandas as pd
from charts_sales import display_chart_country, display_chart_sales

app = Flask(__name__)

@app.route("/")
def w209():
    file="logistics.jpg"
    return render_template("w209.html",file=file)

@app.route("/chart-sales-1")
def display_chart_sales_1():
    chart_json = display_chart_sales()
    return render_template("chart.html", chart_json=chart_json)

@app.route("/chart-sales-2")
def display_chart_sales_2():
    chart_json = display_chart_country()
    return render_template("chart.html", chart_json=chart_json)

@app.route("/chart-sales-3")
def display_chart_sales_3():
    chart_json = display_chart_country()
    return render_template("chart.html", chart_json=chart_json)

@app.route("/chart-customers-1")
def display_chart_customers_1():
    chart_json = display_chart_country()
    return render_template("chart.html", chart_json=chart_json)

@app.route("/chart-customers-2")
def display_chart_customers_2():
    chart_json = display_chart_country()
    return render_template("chart.html", chart_json=chart_json)

@app.route("/chart-customers-3")
def display_chart_customers_3():
    chart_json = display_chart_country()
    return render_template("chart.html", chart_json=chart_json)

@app.route("/chart-delivery-1")
def display_chart_delivery_1():
    chart_json = display_chart_country()
    return render_template("chart.html", chart_json=chart_json)

@app.route("/chart-delivery-2")
def display_chart_delivery_2():
    chart_json = display_chart_country()
    return render_template("chart.html", chart_json=chart_json)

@app.route("/chart-delivery-3")
def display_chart_delivery_3():
    chart_json = display_chart_country()
    return render_template("chart.html", chart_json=chart_json)

if __name__ == "__main__":
    app.run(debug=True)
