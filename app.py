from flask import Flask, render_template
from models import Inventory, Job, Sink

app = Flask(__name__)

@app.route('/')
def home():
    sink = Sink("Stainless Steel Single Bowl Kitchen Sink")
    sink.insert()

    sink = Sink("Rect White Porcelain Bathroom Sink")
    sink.insert()

    sink = Sink("Oval White Porcelain Bathroom Sink")
    sink.insert()


    return render_template('pages/home.html')