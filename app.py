from flask import Flask, render_template
from models import Inventory, Job, Sink
from models import setup_db
from flask_cors import CORS

app = Flask(__name__)
setup_db(app)
CORS(app)

# Returns a list of all jobs in database.
@app.route('/')
def home():
    return render_template('pages/home.html', sinks=(sink.format() for sink in Sink.query.all()))

@app.route('/job', methods=["POST"])
def create_job():
    return render_template('pages/home.html')

@app.route('/job', methods=["GET"])
def create_job_form():
    return render_template('pages/create_job.html')