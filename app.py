from flask import Flask, render_template
from models import Inventory, Job, Sink
from models import setup_db
from flask_cors import CORS

app = Flask(__name__)
setup_db(app)
CORS(app)

@app.route('/')
def home():
    return render_template('pages/home.html', sinks=(sink.format() for sink in Sink.query.all()))