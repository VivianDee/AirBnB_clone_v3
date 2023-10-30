#!/usr/bin/python3
"""Index file"""
from api.v1.views.__init__ import app_views
from flask import jsonify, make_response
from models.__init__ import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', strict_slashes=False)
def app_status():
    """Returns the present status of the app"""
    status = {"status": "OK"}
    return jsonify(status)


@app_views.route('/stats', strict_slashes=False)
def app_stats():
    """Returns the present statis of objects in app storage"""
    amenities = storage.count(Amenity)
    cities = storage.count(City)
    places = storage.count(Place)
    reviews = storage.count(Review)
    states = storage.count(State)
    users = storage.count(User)

    stats = {
          "amenities": amenities,
          "cities": cities,
          "places": places,
          "reviews": reviews,
          "states": states,
          "users": users
        }
    return jsonify(stats)
