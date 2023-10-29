#!/usr/bin/python3
"""Index file"""
from api.v1.views.__init__ import app_views
from flask import jsonify


@app_views.route('/status')
def app_status():
    """Returns the present status of the app"""
    status = {"status" : "OK"}
    return jsonify(status)


@app_views.route('/sats')
def app_stats():
    """Returns the present statis of objects in app storage"""
    status = {"status" : "OK"}
    return jsonify(status)
