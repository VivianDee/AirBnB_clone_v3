#!/usr/bin/python3
"""Flask Application"""
from flask import Flask, make_response, jsonify
from models import storage
from models import *
from api.v1.views.__init__ import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")
cors = CORS(app, resources={'/*': {'origins': '0.0.0.0'}})
host = getenv('HBNB_API_HOST', '0.0.0.0')
port = int(getenv('HBNB_API_PORT', '5000'))
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def teardown_app(error):
    """Tear down the current session"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handles the 404 error on the app"""
    response = jsonify({"error": "Not found"})
    return response, 404


if __name__ == '__main__':
    app.run(host=host, port=port, threaded=True)
