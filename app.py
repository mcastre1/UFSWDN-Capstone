from flask import Flask, jsonify, redirect, render_template, request, abort, url_for, session
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
import os

from models import Inventory, Job, Sink
from models import setup_db
from flask_cors import CORS

from auth.auth import AuthError, requires_auth, get_token_auth_header, verify_decode_jwt

import ast

client_id = os.environ['AUTH0_CLIENT_ID']
client_secret = os.environ['AUTH0_CLIENT_SECRET']
domain = os.environ['AUTH0_DOMAIN']
audience = os.environ['AUTH0_AUDIENCE']
callback = os.environ['AUTH0_CALLBACK']

test = False


app = Flask(__name__)
setup_db(app)
CORS(app)


# Helper method for building authorization url.
# @app.route("/authorization/url", methods=["GET"])
@app.context_processor
def generate_auth_url():

    url = f'https://{domain}/authorize' \
        f'?audience={audience}' \
        f'&response_type=token&client_id=' \
        f'{client_id}&redirect_uri=' \
        f'{callback}'

    return dict(auth_url=url)

# Helper route to set the current users jwt in session.


@app.route('/set_jwt/<string:jwt>', methods=['POST'])
def set_jwt_session(jwt):
    session['user-jwt'] = jwt
    token = get_token_auth_header()
    payload = verify_decode_jwt(token)
    session['user-permissions'] = payload['permissions']

    return jsonify({
        'Success': True
    })

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
    if not test:
        return render_template(
            'pages/home.html',
            jobs=(
                job.format() for job in Job.query.all()),
            session=session)
    else:
        return jsonify({"success": True,
                        "jobs": list(job.format() for job in Job.query.all())})

# This endpoint creates a job through a request form data.


@app.route('/job', methods=["POST"])
@requires_auth(permission="create:job")
def create_job(jwt):
    try:
        form = request.form

        job_name = form['job_name']
        contact_name = form['contact_name']
        contact_phone = form['contact_phone']
        address = form['address']
        material = form['material']
        status = form['status']
        edge_finish = form['edge_finish']
        sinks = ast.literal_eval(form['sinks'])

        job = Job(
            job_name=job_name,
            contact_name=contact_name,
            contact_phone=contact_phone,
            address=address,
            material=material,
            status=status,
            edge_finish=edge_finish,
            sinks=list(sinks))

        job.insert()

        if not test:
            return redirect(url_for('home'))
        else:
            return jsonify({"success": True,
                            "job_id": job.id})
    except BaseException:
        abort(400)


# Endpoint renders the form for creating a job
@app.route('/job', methods=["GET"])
@requires_auth(permission="create:job")
def create_job_form(jwt):
    if not test:
        return render_template('pages/create_job.html', session=session)
    else:
        return jsonify({"success": True})

# Returns a template containing a specific jobs details


@app.route('/job/<int:id>', methods=["GET"])
@requires_auth(permission='read:job-details')
def view_job(jwt, id):
    try:
        job = Job.query.get(int(id))

        if not job:
            abort(404)

        if not test:
            return render_template(
                'pages/view_job.html',
                job=job.format(),
                session=session)
        else:
            return jsonify({"success": True,
                            "job": job.format()})
    except BaseException:
        abort(400)

# Updates given job with new values.


@app.route('/job/<int:id>', methods=["POST"])
@requires_auth(permission="patch:job")
def update_job(jwt, id):
    try:
        form = request.form
        job = Job.query.get(int(id))

        if not job:
            abort(404)

        job.job_name = form['job_name']
        job.contact_name = form['contact_name']
        job.contact_phone = form['contact_phone']
        job.address = form['address']
        job.material = form['material']
        job.status = form['status']
        job.edge_finish = form['edge_finish']
        job.sinks = ast.literal_eval(form['sinks'])

        job.update()

        if not test:
            return redirect(url_for('home'))
        else:
            return jsonify({"success": True,
                            "job": job.format()})

    except BaseException:
        abort(400)

# Deletes a specific job


@app.route('/job/<int:id>/delete_job', methods=["DELETE"])
@requires_auth(permission="delete:job")
def delete_job(jwt, id):
    try:
        job = Job.query.get(int(id))
        if not job:
            abort(404)

        job.delete()

        if not test:
            return redirect(url_for('home'))
        else:
            return jsonify({"success": True,
                            "job": job.format()['id']})
    except BaseException:
        return (400)

# Returns template containing all inventory items.


@app.route('/inventory', methods=["GET"])
@requires_auth(permission="read:inventory")
def inventory(jwt):
    if not test:
        return render_template(
            '/pages/inventory.html',
            inventory=(
                item.format() for item in Inventory.query.all()),
            session=session)
    else:
        return jsonify({"success": True, "inventory": [
                       item.format() for item in Inventory.query.all()]})

# Returns a template containing a specific inventory item's details


@app.route('/inventory/<int:id>', methods=["GET"])
@requires_auth("read:inventory_item")
def view_inventory_item(jwt, id):
    try:
        inventory_item = Inventory.query.get(int(id))
        if not inventory_item:
            abort(404)
        if not test:
            return render_template(
                '/pages/view_inventory_item.html',
                inventory_item=inventory_item.format(),
                session=session)
        else:
            return jsonify({"success": True,
                            "inventory_item": inventory_item.format()})
    except BaseException:
        abort(400)

# Updates a specific inventory item with new values.


@app.route('/inventory/<int:id>', methods=["POST"])
@requires_auth("patch:inventory_item")
def update_inventory_item(jwt, id):
    try:
        form = request.form
        count = int(form['count'])

        inventory_item = Inventory.query.get(int(id))
        if not inventory_item:
            abort(404)

        inventory_item.count = count

        inventory_item.update()
        if not test:
            return redirect(url_for('inventory'))
        else:
            return jsonify({"success": True,
                            "inventory_item": inventory_item.format()})
    except BaseException:
        abort(400)

# Returns the form template for inventory item creation


@app.route('/inventory/add', methods=["GET"])
@requires_auth(permission="create:inventory_item")
def add_inventory_item_form(jwt):
    if not test:
        return render_template(
            '/pages/add_inventory_item.html',
            session=session)
    else:
        return jsonify({"success": True})

# Creates a new inventory_item.


@app.route('/inventory/add', methods=["POST"])
@requires_auth(permission="create:inventory_item")
def add_inventory_item(jwt):

    try:
        form = request.form

        item = Inventory(sink_id=int(
            form['sink_id']), count=int(form['count']))
        item.insert()

        if not test:
            return render_template(
                '/pages/inventory.html',
                inventory=(
                    item.format() for item in Inventory.query.all()),
                session=session)
        else:
            return jsonify({"success": True, "inventory_items": [inventory_item.format(
            ) for inventory_item in Inventory.query.all()], "inventory_item_id": item.id})
    except BaseException:
        abort(400)


@app.route('/inventory/<int:id>/delete_inventory_item', methods=["DELETE"])
@requires_auth(permission="delete:inventory_item")
def delete_inventory_item(jwt, id):
    try:
        inventory_item = Inventory.query.get(int(id))

        if not inventory_item:
            abort(404)

        inventory_item.delete()

        if not test:
            return redirect(url_for('inventory'))
        else:
            return jsonify({"success": True,
                            "inventory_item_id": inventory_item.format()['id'],
                            "inventory_items": [inventory_item.format() for inventory_item in Inventory.query.all()]})
    except BaseException:
        abort(400)

# Returns a template with all available sinks


@app.route('/sinks', methods=["GET"])
@requires_auth(permission="read:sinks")
def sinks(jwt):
    if not test:
        return render_template(
            '/pages/sinks.html',
            sinks=(
                sink.format() for sink in Sink.query.all()),
            session=session)
    else:
        return jsonify({"success": True, "sinks": [
                       sink.format() for sink in Sink.query.all()]})

# Returns a template with a specific sink details.


@app.route('/sinks/<int:id>', methods=["GET"])
@requires_auth(permission="read:sink")
def view_sink(jwt, id):
    try:
        sink = Sink.query.get(int(id))
        if not sink:
            abort(404)
        if not test:
            return render_template(
                '/pages/view_sink.html',
                sink=sink.format(),
                session=session)
        else:
            return jsonify({"success": True,
                            "sink": sink.format()})
    except BaseException:
        abort(400)

# Updates a specific sink details.


@app.route('/sinks/<int:id>', methods=["POST"])
@requires_auth(permission="patch:sink")
def update_sink(jwt, id):
    try:
        form = request.form
        sink = Sink.query.get(int(id))

        if not sink:
            abort(404)

        description = form['description']

        sink.description = description

        sink.update()
        if not test:
            return redirect(url_for('sinks'))
        else:
            return jsonify({"success": True,
                            "sink": sink.format()})
    except BaseException:
        abort(400)


@app.route('/sinks/<int:id>/delete_sink', methods=["DELETE"])
@requires_auth(permission="delete:sink")
def delete_sink(jwt, id):
    try:
        sink = Sink.query.get(int(id))

        if not sink:
            abort(404)

        sink.delete()

        if not test:
            return redirect(url_for('sinks'))
        else:
            return jsonify({"success": True,
                            "sink": sink.format()['id']})

    except BaseException:
        abort(400)

# Returns a template containing a form for sink creation.


@app.route('/sinks/add', methods=["GET"])
@requires_auth(permission="create:sink")
def add_sink_form(jwt):
    if not test:
        return render_template('/pages/add_sink.html', session=session)
    else:
        return jsonify({"success": True})

# Creates a new sink.


@app.route('/sinks/add', methods=["POST"])
@requires_auth(permission="create:sink")
def add_sink(jwt):
    try:
        form = request.form
        description = form['description']

        sink = Sink(description=description)
        sink.insert()

        if not test:
            return render_template(
                '/pages/sinks.html',
                sinks=(
                    sink.format() for sink in Sink.query.all()),
                session=session)
        else:
            return jsonify({"success": True,
                            "sinks": [sink.format() for sink in Sink.query.all()],
                            'sink_id': sink.id})
    except BaseException:
        abort(400)


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
