from flask import Flask, jsonify, redirect, render_template, request, abort, url_for, session
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
import os

from models import Inventory, Job, Sink
from models import setup_db
from flask_cors import CORS

from .auth.auth import AuthError, requires_auth

import ast

client_id = os.environ['AUTH0_CLIENT_ID']
client_secret = os.environ['AUTH0_CLIENT_SECRET']
domain = os.environ['AUTH0_DOMAIN']

app = Flask(__name__)
setup_db(app)
CORS(app)


#Helper method for building authorization url.
#@app.route("/authorization/url", methods=["GET"])
@app.context_processor
def generate_auth_url():
    
    AUTH0_JWT_API_AUDIENCE = "capstoneAPI"
    AUTH0_CALLBACK_URL = "http://127.0.0.1:5000/"

    url = f'https://{domain}/authorize' \
        f'?audience={AUTH0_JWT_API_AUDIENCE}' \
        f'&response_type=token&client_id=' \
        f'{client_id}&redirect_uri=' \
        f'{AUTH0_CALLBACK_URL}'
        
    return dict(auth_url=url)

# Helper route to set the current users jwt in session.
@app.route('/set_jwt/<string:jwt>', methods=['POST'])
def set_jwt_session(jwt):
    session['user-jwt'] = jwt
    return('/')

# Route for logging out of auth0 service and clearing off session.
@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + 'dev-nmyxk7hftomeflrd.us.auth0.com'
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": "PYEPrbcSnWPlTrIAjvTjp2caniJnSotT",
            },
            quote_via=quote_plus,
        )
    )

# Returns a list of all jobs in database.
@app.route('/')
def home():
    return render_template('pages/home.html', jobs=(job.format() for job in Job.query.all()), session=session.get('user-jwt'))

# 
@app.route('/job', methods=["POST"])
def create_job():
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
    return render_template('pages/create_job.html', session=session.get('user'))

@app.route('/job/<int:id>', methods=["GET"])
def view_job(id):
    job = Job.query.get(int(id))
    return render_template('pages/view_job.html', job=job.format(), session=session.get('user'))

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
    return render_template('/pages/inventory.html', inventory=(item.format() for item in Inventory.query.all()), session=session.get('user'))

@app.route('/inventory/<int:id>', methods=["GET"])
def view_inventory_item(id):
    inventory_item = Inventory.query.get(int(id))
    return render_template('/pages/view_inventory_item.html', inventory_item = inventory_item.format(), session=session.get('user'))

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
    return render_template('/pages/add_inventory_item.html', session=session.get('user'))

@app.route('/inventory/add', methods=["POST"])
def add_inventory_item():
    form = request.form
    
    item = Inventory(sink_id=int(form['sink_id']), count=int(form['count']))
    item.insert()

    return render_template('/pages/inventory.html', inventory=(item.format() for item in Inventory.query.all()), session=session.get('user'))

@app.route('/sinks',methods=["GET"])
def sinks():
    return render_template('/pages/sinks.html', sinks=(sink.format() for sink in Sink.query.all()), session=session.get('user'))

@app.route('/sinks/<int:id>', methods=["GET"])
def view_sink(id):
    sink = Sink.query.get(int(id))

    return render_template('/pages/view_sink.html', sink=sink.format(), session=session.get('user'))

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
    return render_template('/pages/add_sink.html', session=session.get('user'))

@app.route('/sinks/add', methods=["POST"])
def add_sink():
    form = request.form
    description = form['description']

    sink = Sink(description=description)
    sink.insert()

    return render_template('/pages/sinks.html', sinks=(sink.format() for sink in Sink.query.all()), session=session.get('user'))


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": 'Unathorized'
    }), 401


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": 'Internal Server Error'
    }), 500


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": 'Bad Request'
    }), 400


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": 'Method Not Allowed'
    }), 405