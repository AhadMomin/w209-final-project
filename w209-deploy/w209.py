from flask import Flask, render_template
import altair as alt
import pandas as pd

from logging.config import dictConfig

from otd_page1 import create_shipper_customer_view
from otd_page2 import create_order_attributes_view
from otd_page3 import create_shipper_customer_map


# Setup Flask log file.
dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "default",
            },
            "file": {
                "class": "logging.FileHandler",
                "filename": "/home/ngchuchi/w209/flask.log",
                "formatter": "default",
            },
        },
        "root": {"level": "DEBUG", "handlers": ["console", "file"]},
    }
)


app = Flask(__name__)

@app.route("/")
def w209():
   app.logger.debug("calling root....")
   file="about9.jpg"
   return render_template("w209.html",file=file)

@app.route("/pandas-api/")
def api():
   d = pd.DataFrame([{"a": "b"}])
   return d.to_dict()

@app.route("/otd-page1/")
def otd_page1():
  app.logger.debug("Calling otd_page1...")
  chart_json = create_shipper_customer_view()
  return render_template("chart1.html", chart_json=chart_json)

@app.route("/otd-page2/")
def otd_page2():
  app.logger.debug("Calling otd_page2...")
  chart_json = create_order_attributes_view()
  return render_template("chart2.html", chart_json=chart_json)

@app.route("/otd-page3/")
def otd_page3():
  app.logger.debug("Calling otd_page3...")
  chart_json = create_shipper_customer_map()
  return render_template("chart3.html", chart_json=chart_json)


if __name__ == "__main__":
  app.logger.debug("Starting app....")
  app.run()
