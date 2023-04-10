from flask import Flask, redirect, render_template, request, abort, flash, url_for
from models import Inventory, Job, Sink
from models import setup_db
from flask_cors import CORS
import ast

app = Flask(__name__)
setup_db(app)
CORS(app)

# Returns a list of all jobs in database.
@app.route('/')
def home():
    print(Job.query.all())
    return render_template('pages/home.html', jobs=(job.format() for job in Job.query.all()))

@app.route('/job', methods=["POST"])
def create_job():
    #print(request.get_json())
    try:
        form = request.form
        print(form)
        job_name = form['job_name']
        contact_name = form['contact_name']
        contact_phone = form['contact_phone']
        address = form['address']
        material = form['material']
        status = form['status']
        edge_finish = form['edge_finish']
        sinks = ast.literal_eval(form['sinks'])
        print(sinks)

        job = Job(job_name=job_name, contact_name=contact_name, contact_phone=contact_phone, address=address,
                  material=material, status=status, edge_finish=edge_finish, sinks=list(sinks))   
        job.insert()
        #flash(f"Succesfully Added {job_name} to the jobs list.")
        return redirect(url_for('home'))
    except :
        abort(400)

    

@app.route('/job', methods=["GET"])
def create_job_form():
    return render_template('pages/create_job.html')

@app.route('/job/<int:id>', methods=["GET"])
def view_job(id):
    job = Job.query.get(int(id))
    return render_template('pages/view_job.html', job=job.format())

@app.route('/job/<int:id>', methods=["POST"])
def update_job(id):
    try:
        form = request.form
        job = Job.query.get(int(id))

        job.job_name = form['job_name']
        job.contact_name = form['contact_name']
        job.contact_phone = form['contact_phone']
        job.address = form['address']
        job.material = form['material']
        job.status = form['status']
        job.edge_finish = form['edge_finish']
        job.sinks = ast.literal_eval(form['sinks'])

        job.update()
        #flash(f"Succesfully Added {job_name} to the jobs list.")
        return redirect(url_for('home'))
    except :
        abort(400)

@app.route('/job/<int:id>/delete_job', methods=["DELETE"])
def delete_job(id):
    job = Job.query.get(int(id))
    job.delete()

    print("job deleted")
    return redirect(url_for('home'))

@app.route('/inventory', methods=["GET"])
def inventory():
    return render_template('/pages/inventory.html', inventory=(item.format() for item in Inventory.query.all()))

@app.route('/inventory/<int:id>', methods=["GET"])
def view_inventory_item(id):
    inventory_item = Inventory.query.get(int(id))
    return render_template('/pages/view_inventory_item.html', inventory_item = inventory_item.format())

@app.route('/inventory/<int:id>', methods=["POST"])
def update_inventory_item(id):
    form = request.form
    count = int(form['count'])

    inventory_item = Inventory.query.get(int(id))
    inventory_item.count = count

    inventory_item.update()

    return redirect(url_for('inventory'))


@app.route('/inventory/add', methods=["GET"])
def add_inventory_item_form():
    return render_template('/pages/add_inventory_item.html')

@app.route('/inventory/add', methods=["POST"])
def add_inventory_item():
    form = request.form
    
    item = Inventory(sink_id=int(form['sink_id']), count=int(form['count']))
    item.insert()

    return render_template('/pages/inventory.html', inventory=(item.format() for item in Inventory.query.all()))

@app.route('/sinks',methods=["GET"])
def sinks():
    return render_template('/pages/sinks.html', sinks=(sink.format() for sink in Sink.query.all()))

@app.route('/sinks/<int:id>', methods=["GET"])
def view_sink(id):
    sink = Sink.query.get(int(id))

    return render_template('/pages/view_sink.html', sink=sink.format())

@app.route('/sinks/<int:id>', methods=["POST"])
def update_sink(id):
    form = request.form
    sink = Sink.query.get(int(id))

    description = form['description']

    sink.description = description

    sink.update()

    return redirect(url_for('sinks')) 

@app.route('/sinks/add', methods=["GET"])
def add_sink_form():
    return render_template('/pages/add_sink.html')

@app.route('/sinks/add', methods=["POST"])
def add_sink():
    form = request.form
    description = form['description']

    sink = Sink(description=description)
    sink.insert()

    return render_template('/pages/sinks.html', sinks=(sink.format() for sink in Sink.query.all()))
