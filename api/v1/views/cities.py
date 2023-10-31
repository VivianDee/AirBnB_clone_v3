#!/usr/bin/python3
"""City view"""
from api.v1.views.__init__ import app_views
from flask import jsonify, make_response, abort, request
from models.__init__ import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def retrieve_cities_in_state(state_id):
    """Retrieves the list of all City objects of a State"""
    all_cities = storage.all(City).values()

    cities_in_state = [city.to_dict()
                       for city in all_cities if city.state_id == state_id]

    if len(cities_in_state) == 0:
        abort(404)
    return jsonify(cities_in_state)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def retrieve_city(city_id):
    """Retrieves a City object"""
    city_obj = storage.get(City, city_id)

    if not city_obj:
        abort(404)

    return jsonify(city_obj.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object"""
    city_obj = storage.get(City, city_id)

    if not city_obj:
        abort(404)

    storage.delete(city_obj)
    storage.save()

    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """Creates a City object"""
    request_data = request.get_json()
    if not request_data:
        abort(400, 'Not a JSON')
    if 'name' not in request_data:
        abort(400, 'Missing name')

    state_obj = storage.get(State, state_id)

    if not state_obj:
        abort(404)

    new_instance = City(name=request_data['name'], state_id=state_id)
    new_instance.save()

    return jsonify(new_instance.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a City object"""
    city_obj = storage.get(City, city_id)

    if not city_obj:
        abort(404)

    request_data = request.get_json()
    if not request_data:
        abort(400, 'Not a JSON')

    for key in ['id', 'state_id', 'created_at', 'updated_at']:
        if key in request_data.keys():
            del request_data[key]

    storage.reload()

    for key, value in request_data.items():
        setattr(city_obj, key, value)
    storage.save()
    storage.reload()

    return jsonify(city_obj.to_dict()), 200
