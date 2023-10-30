#!/usr/bin/python3
"""User view"""
from api.v1.views.__init__ import app_views
from flask import jsonify, make_response, abort, request
from models.__init__ import storage
from models.city import City
from models.state import State
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def retrieve_all_users():
    """Retrieves the list of all User objects"""
    all_users = storage.all(User).values()

    users = [user.to_dict() for user in all_users]

    if len(users) == 0:
        abort(404)
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def retrieve_user(user_id):
    """Retrieves a User object"""
    storage.save()
    storage.reload()
    user_obj = storage.get(User, user_id)

    if not user_obj:
        abort(404)

    return jsonify(user_obj.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object"""
    user_obj = storage.get(User, user_id)

    if not user_obj:
        abort(404)

    storage.delete(user_obj)
    storage.save()

    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a User object"""
    request_data = request.get_json()
    if not request_data:
        abort(400, 'Not a JSON')
    if 'email' not in request_data:
        abort(400, 'Missing email')
    if 'password' not in request_data:
        abort(400, 'Missing password')

    new_instance = User(
        email=request_data['email'], password=request_data['password'])
    new_instance.save()

    return jsonify(new_instance.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a User object"""
    user_obj = storage.get(User, user_id)

    if not user_obj:
        abort(404)

    request_data = request.get_json()
    if not request_data:
        abort(400, 'Not a JSON')

    for key in ['id', 'email', 'created_at', 'updated_at']:
        if key in request_data.keys():
            del request_data[key]

    storage.reload()

    for key, value in request_data.items():
        setattr(user_obj, key, value)
    storage.save()
    storage.reload()

    return jsonify(user_obj.to_dict()), 200
