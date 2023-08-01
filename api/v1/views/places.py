#!/usr/bin/python3
"""view for City objects that handles all default RESTFul API actions"""

from models.city import City
from models.place import Place
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, request, jsonify


@app_views.route("/cities/<city_id>/places", methods=['GET', 'POST'])
def list_places(city_id):
    """list of all City objects by State id"""
    if request.method == 'POST':
        return create_place(city_id)
    try:
        city = storage.get(City, city_id)
    except Exception:
        abort(404)
    places = storage.all(Place)
    place_list = []
    for key, value in places.items():
        if city.id == value.to_dict().get('city_id'):
            place_list.append(value.to_dict())
    return jsonify(place_list)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place_by_id(place_id):
    """Retrieves a City object by id"""
    try:
        place = storage.get(Place, place_id)
        place_dict = place.to_dict()
    except Exception:
        abort(404)
    return jsonify(place_dict)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Deletes a Place by id"""
    try:
        place = storage.get(Place, place_id)
        storage.delete(place)
        storage.save()
        res = {}
    except Exception:
        abort(404)
    return jsonify(res), 200


def create_place(city_id):
    """Creates a Place"""
    try:
        city = storage.get(City, city_id)
        if city is None:
            raise AttributeError
    except Exception:
        abort(404)
    try:
        name = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')
    if 'user_id' not in name.keys() or name['user_id'] is None:
        abort(400, 'Missing user_id')
    try:
        usr = storage.get(User, name['user_id'])
        if usr is None:
            raise AttributeError
    except Exception:
        abort(404)
    if 'name' not in name.keys() or name['name'] is None:
        abort(400, 'Missing name')
    n_place = {'name': name['name'], 'user_id': usr.id, 'city_id': city.id}
    place = Place(**n_place)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=["PUT"])
def update_place(place_id):
    """Updates a Place by id"""
    try:
        place = storage.get(Place, place_id)
    except Exception:
        abort(404)
    try:
        name = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')
    for key, value in name.items():
        if (key not in
                ('id', 'user_id', 'city_id', 'created_at', 'updated_at')):
            setattr(place, key, value)
        storage.save()
    return jsonify(place.to_dict()), 200
