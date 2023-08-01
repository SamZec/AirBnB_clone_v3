#!/usr/bin/python3
"""view for User objects that handles all default RESTFul API actions"""

from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, request, jsonify


@app_views.route("/users", methods=['GET'])
def list_users():
    """list of all User objects"""
    user = storage.all(User)
    user_list = []
    for key, value in user.items():
        user_list.append(value.to_dict())
    return jsonify(user_list)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    """Retrieves a User object by id"""
    try:
        user = storage.get(User, user_id)
        user_dict = user.to_dict()
    except Exception:
        abort(404)
    return jsonify(user_dict)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a User by id"""
    try:
        user = storage.get(User, user_id)
        storage.delete(user)
        storage.save()
        res = {}
    except Exception:
        abort(404)
    return jsonify(res), 200


@app_views.route('/users', methods=['POST'])
def create_user():
    """Creates a User"""
    try:
        name = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')
    if 'email' not in name.keys():
        abort(400, 'Missing email')
    if 'password' not in name.keys():
        abort(400, 'Missing password')
    user = User(**name)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=["PUT"])
def update_user(user_id):
    """Updates a User by id"""
    try:
        user = storage.get(User, user_id)
    except Exception:
        abort(404)
    name = request.get_json()
    if name is None:
        abort(400, 'Not a JSON')
    for key, value in name.items():
        if (key not in ('id', 'created_at', 'updated_at')):
            setattr(user, key, value)
        storage.save()
    return jsonify(user.to_dict()), 200
