#!/usr/bin/python3
"""State objects that handles all default RESTFul API actions"""

from flask import jsonify, request
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest

from api.v1.views import app_views
from models import storage
from models.state import State


API_METHODS = ['GET', 'DELETE', 'POST', 'PUT']
'''API allowed methods for the /states endpoint.'''


@app_views.route('/states', methods=API_METHODS)
@app_views.route('/states/<state_id>', methods=API_METHODS)
def handle_states(state_id=None):
    '''The endpoint method handler for the states endpoint.
    '''
    endpoint_handlers = {
        'GET': get_state,
        'DELETE': remove_state,
        'POST': add_state,
        'PUT': update_state,
    }

    if request.method in endpoint_handlers:
        return endpoint_handlers[request.method](state_id)
    raise MethodNotAllowed(list(endpoint_handlers.keys()))


def get_state(state_id=None):
    '''Gets the state with the provided id or all states.
    '''
    states = storage.all(State).values()
    if state_id:
        response = filterstates(state_id=state_id, states=states)
        if response:
            return jsonify(response[0].to_dict())
        raise NotFound()
    states = list(map(lambda x: x.to_dict(), states))
    return jsonify(states)


def remove_state(state_id=None):
    '''Removes a state with the provided id.
    '''
    states = storage.all(State).values()
    res = filterstates(state_id=state_id, states=states)
    if res:
        storage.delete(res[0])
        storage.save()
        return jsonify({}), 200
    raise NotFound()


def add_state(state_id=None):
    '''Adds a new state.
    '''
    data = request.get_json()
    if type(data) is not dict:
        raise BadRequest(description='Not a JSON')
    if 'name' not in data:
        raise BadRequest(description='Missing name')
    newstate = State(**data)
    newstate.save()
    return jsonify(newstate.to_dict()), 201


def update_state(state_id=None):
    '''Updates the state with the given id.
    '''
    xkeys = ('id', 'created_at', 'updated_at')
    states = storage.all(State).values()
    res = filterstates(state_id=state_id, states=states)
    if res:
        data = request.get_json()
        if type(data) is not dict:
            raise BadRequest(description='Not a JSON')
        previous_state = res[0]
        for key, value in data.items():
            if key not in xkeys:
                setattr(previous_state, key, value)
        previous_state.save()
        return jsonify(previous_state.to_dict()), 200
    raise NotFound()


def filterstates(state_id, states):
    """Returns a new state list based on provided Id"""
    res = list(filter(lambda x: x.id == state_id, states))
    return res
