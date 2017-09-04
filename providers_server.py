# Taken with some modification from Backend Exercise #
import json

from flask import Flask, request, jsonify, redirect, url_for, make_response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path="")
# Change the assigned string if credentials and/or port are unavailable
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:hayesj3@localhost:5432/Login'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Gives a warning if not set
app.secret_key = '\xd0\xf9\x11\xd9\x84}\xb4\xd0J\x9dD\x10\xb9\t\xb6\x10%\xc3\xcbv\x9f\xfd\xbf\xac'
db = SQLAlchemy(app)


class Provider(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20))  # non-unique names for simplicity
    lname = db.Column(db.String(20))  # non-unique names for simplicity
    email = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(40))

    def __init__(self, fname, lname, email, password):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.password = password

    def __repr__(self):
        return '<Provider %r %r>' % self.fname % self.lname


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Provider):
            return {
                "id": obj.id,
                "fname": obj.fname,
                "lname": obj.lname,
                "email": obj.email,
            }
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


@app.route('/')
def index():
    return redirect(url_for('static', filename="index.html"))


@app.route('/providers/login', methods=['POST'])
def login():
    dct = request.get_json(force=True)
    email = dct["email"]
    password = dct["password"]
    provider = Provider.query.filter_by(email=email,password=password).first()

    if provider is None:
        return make_response(jsonify({'error': 'Bad login credentials'}), 403)
    return make_response(jsonify({'status': 'Ok'}), 200)


@app.route('/providers/signup', methods=['POST'])
def sign_up():
    dct = request.get_json(force=True)
    fname = dct["fname"]
    lname = dct["lname"]
    email = dct["email"]
    password = dct["password"]

    provider = Provider.query.filter_by(email=email).first()
    if provider is None:    # email is available
        provider = Provider(fname, lname, email, password)
        db.session.add(provider)
        db.session.commit()
        return make_response(jsonify({'status': 'Created'}), 201)
    return make_response(jsonify({'error': 'Conflict: email already in use'}), 409)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(401)
def unauthorized(error):
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)


@app.errorhandler(403)
def forbidden(error):
    return make_response(jsonify({'error': 'Forbidden'}), 403)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(409)
def conflict(error):
    return make_response(jsonify({'error': 'Conflict'}), 409)


if __name__ == '__main__':
# Uncomment on first run to setup the database schema
# A database named "Login" must be accessible on port 5432 with
# username "postgres" and password "hayesj3" must already exist
    #db.create_all()
    app.run(debug=False)
