from flask import Flask, redirect, render_template, request, abort, flash, url_for
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
    #print(request.get_json())
    try:
        form = request.form
        job_name = form['job_name']
        contact_name = form['contact_name']
        contact_phone = form['contact_phone']
        address = form['address']
        material = form['material']
        status = form['status']
        edge_finish = form['edge_finish']
        sinks = form['sinks']

        job = Job(job_name=job_name, contact_name=contact_name, contact_phone=contact_phone, address=address,
                  material=material, status=status, edge_finish=edge_finish, sinks=sinks)   
         
        job.insert()
        #flash("Created succesfully!")
        return render_template('pages/home.html')
    except :
        abort(400)

    

@app.route('/job', methods=["GET"])
def create_job_form():
    return render_template('pages/create_job.html')