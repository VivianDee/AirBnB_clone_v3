#!/usr/bin/python3
"""My Flask Application"""
from flask import Flask, make_response, jsonify
from models import storage
from models import *
from api.v1.views.__init__ import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


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
    try:
        host = getenv(HBNB_API_HOST)
        port = getenv(HBNB_API_PORT)
    except NameError:
        host = '0.0.0.0'
        port = 5000

    app.run(host=host, port=port, threaded=True)
