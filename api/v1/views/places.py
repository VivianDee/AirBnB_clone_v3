#!/usr/bin/python3
"""Place view"""
from api.v1.views.__init__ import app_views
from flask import jsonify, make_response, abort, request
from models.__init__ import storage
from models.city import City
from models.state import State
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def retrieve_places_in_city(city_id):
    """Retrieves the list of all Place objects of a City"""
    all_places = storage.all(Place).values()

    places_in_city = [place.to_dict()
                      for place in all_places if place.city_id == city_id]

    if len(places_in_city) == 0:
        abort(404)
    return jsonify(places_in_city)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def retrieve_place(place_id):
    """Retrieves a Place object"""
    place_obj = storage.get(Place, place_id)

    if not place_obj:
        abort(404)

    return jsonify(place_obj.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place_obj = storage.get(Place, place_id)

    if not place_obj:
        abort(404)

    storage.delete(place_obj)
    storage.save()

    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place object"""
    request_data = request.get_json()
    if not request_data:
        abort(400, 'Not a JSON')
    if 'user_id' not in request_data:
        abort(400, 'Missing user_id')
    if 'name' not in request_data:
        abort(400, 'Missing name')

    user_obj = storage.get(User, request_data['user_id'])
    city_obj = storage.get(City, city_id)

    if not user_obj or not city_obj:
        abort(404)

    new_instance = Place(
        name=request_data['name'], city_id=city_id,
        user_id=request_data['user_id'])
    new_instance.save()

    return jsonify(new_instance.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place_obj = storage.get(Place, place_id)

    if not place_obj:
        abort(404)

    request_data = request.get_json()
    if not request_data:
        abort(400, 'Not a JSON')

    for key in ['id', 'user_id', 'created_at', 'updated_at']:
        if key in request_data.keys():
            del request_data[key]

    storage.reload()

    for key, value in request_data.items():
        setattr(place_obj, key, value)
    storage.save()
    storage.reload()

    return jsonify(place_obj.to_dict()), 200
