#!/usr/bin/python3
"""view for State objects that handles all default RESTFul API actions"""

from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, request, jsonify
import json


@app_views.route("/states", methods=['GET'])
def list_states():
    """list of all State objects"""
    states = storage.all(State)
    states_list = []
    for key, value in states.items():
        states_list.append(value.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_sate_by_id(state_id):
    """Retrieves a State object by id"""
    try:
        state = storage.get(State, state_id)
        state_dict = state.to_dict()
    except Exception:
        abort(404)
    return jsonify(state_dict)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Deletes a State by id"""
    try:
        state = storage.get(State, state_id)
        if state is None:
            raise AttributeError
        storage.delete(state)
        storage.save()
        res = {}
    except Exception:
        abort(404)
    return jsonify(res)


@app_views.route('/states/', methods=['POST'])
def create_state():
    """Creates a State"""
    try:
        name = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')
    if 'name' not in name.keys() or name['name'] is None:
        abort(400, 'Missing name')
    state = State(name=name['name'])
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=["PUT"])
def update_state(state_id):
    """Updates a State by id"""
    try:
        state = storage.get(State, state_id)
        if state is None:
            raise AttributeError
    except Exception:
        abort(404)
    try:
        name = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')
    if 'name' not in name.keys() or name is None:
        abort(400, 'Missing name')
    for key, value in name.items():
        if (key not in ('id', 'created_at', 'updated_at')):
            setattr(state, key, value)
        storage.save()
    return jsonify(state.to_dict()), 200
