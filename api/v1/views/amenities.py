#!/usr/bin/python3
'''Contains the amenities view for the API.'''
from flask import request, jsonify
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


API_METHODS = ['GET', 'DELETE', 'POST', 'PUT']
'''API methods allowed for the /amenities endpoint.'''


@app_views.route('/amenities', methods=API_METHODS)
@app_views.route('/amenities/<amenity_id>', methods=API_METHODS)
def handle_amenities(amenity_id=None):
    '''The api method handler for the amenities endpoint.
    '''
    handlers = {
        'GET': get_amenities,
        'DELETE': remove_amenity,
        'POST': add_amenity,
        'PUT': update_amenity,
    }
    if request.method in handlers:
        return handlers[request.method](amenity_id)
    raise MethodNotAllowed(list(handlers.keys()))


def get_amenities(amenity_id=None):
    '''Gets the amenity with the provided id or all amenities.
    '''
    amenities = storage.all(Amenity).values()
    if amenity_id:
        res = filteramenities(amenity_id=amenity_id, amenities=amenities)
        if res:
            return jsonify(res[0].to_dict())
        raise NotFound()
    amenities = list(map(lambda x: x.to_dict(), amenities))
    return jsonify(amenities)


def remove_amenity(amenity_id=None):
    '''Removes a amenity with the provided id.
    '''
    amenities = storage.all(Amenity).values()
    res = filteramenities(amenity_id=amenity_id, amenities=amenities)
    if res:
        storage.delete(res[0])
        storage.save()
        return jsonify({}), 200
    raise NotFound()


def add_amenity(amenity_id=None):
    '''Adds a new amenity.
    '''
    data = request.get_json()
    if type(data) is not dict:
        raise BadRequest(description='Not a JSON')
    if 'name' not in data:
        raise BadRequest(description='Missing name')
    new_amenity = Amenity(**data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


def update_amenity(amenity_id=None):
    '''Updates the amenity with the provided id.
    '''
    xkeys = ('id', 'created_at', 'updated_at')
    amenities = storage.all(Amenity).values()
    res = filteramenities(amenity_id=amenity_id, amenities=amenities)
    if res:
        data = request.get_json()
        if type(data) is not dict:
            raise BadRequest(description='Not a JSON')
        previous_amenities = res[0]
        for key, value in data.items():
            if key not in xkeys:
                setattr(previous_amenities, key, value)
        previous_amenities.save()
        return jsonify(previous_amenities.to_dict()), 200
    raise NotFound()


def filteramenities(amenity_id, amenities):
    """Returns a new amenty list based on provided Id"""
    res = list(filter(lambda x: x.id == amenity_id, amenities))
    return res
