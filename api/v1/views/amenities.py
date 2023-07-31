#!/usr/bin/python3
"""view for Amenity objects that handles all default RESTFul API actions"""

from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, request, jsonify


@app_views.route("/amenities", methods=['GET'])
def list_amenities():
    """list of all Amenity objects"""
    amenities = storage.all(Amenity)
    amnities_list = []
    for key, value in amenities.items():
        amnities_list.append(value.to_dict())
    return jsonify(amnities_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity_by_id(amenity_id):
    """Retrieves an Amenity object by id"""
    try:
        amenity = storage.get(Amenity, amenity_id)
        amenity_dict = amenity.to_dict()
    except Exception:
        abort(404)
    return jsonify(amenity_dict)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """Deletes an Amenity by id"""
    try:
        amenity = storage.get(Amenity, amenity_id)
        storage.delete(amenity)
        storage.save()
        res = {}
    except Exception:
        abort(404)
    return jsonify(res), 200


@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """Creates an Amenity"""
    try:
        name = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')
    if 'name' not in name.keys():
        abort(400, 'Missing name')
    amenity = Amenity(**name)
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=["PUT"])
def update_amenity(amenity_id):
    """Updates an Amenity by id"""
    try:
        amenity = storage.get(Amenity, amenity_id)
    except Exception:
        abort(404)
    name = request.get_json()
    if name is None:
        abort(400, 'Not a JSON')
    for key, value in name.items():
        if (key not in ('id', 'created_at', 'updated_at')):
            setattr(amenity, key, value)
        storage.save()
    return jsonify(amenity.to_dict()), 200
