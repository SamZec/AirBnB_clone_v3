#!/usr/bin/python3
"""view for City objects that handles all default RESTFul API actions"""

from models.city import City
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, request, jsonify


@app_views.route("/states/<state_id>/cities", methods=['GET', 'POST'])
def list_cities(state_id):
    """list of all City objects by State id"""
    if request.method == 'POST':
        return create_city(state_id)
    try:
        state = storage.get(State, state_id)
    except Exception:
        abort(404)
    cities = storage.all(City)
    cities_list = []
    for key, value in cities.items():
        if state.id == value.to_dict().get('state_id'):
            cities_list.append(value.to_dict())
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city_by_id(city_id):
    """Retrieves a City object by id"""
    try:
        city = storage.get(City, city_id)
        city_dict = city.to_dict()
    except Exception:
        abort(404)
    return jsonify(city_dict)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Deletes a City by id"""
    try:
        city = storage.get(City, city_id)
        storage.delete(city)
        storage.save()
        res = {}
    except Exception:
        abort(404)
    return jsonify(res), 200


def create_city(state_id):
    """Creates a City"""
    print(state_id)
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
    if 'name' not in name.keys() or name['name'] is None:
        abort(400, 'Missing name')
    create_city = {'name': name['name'], 'state_id': state.id}
    city = City(**create_city)
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=["PUT"])
def update_city(city_id):
    """Updates a City by id"""
    try:
        city = storage.get(City, city_id)
    except Exception:
        abort(404)
    try:
        name = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')
    for key, value in name.items():
        if (key not in ('id', 'created_at', 'updated_at')):
            setattr(city, key, value)
        storage.save()
    return jsonify(city.to_dict()), 200
