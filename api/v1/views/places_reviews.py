#!/usr/bin/python3
"""view for Review objects that handles all default RESTFul API actions"""

from models.place import Place
from models.user import User
from models.review import Review
from models import storage
from api.v1.views import app_views
from flask import abort, request, jsonify


@app_views.route("/places/<place_id>/reviews", methods=['GET', 'POST'])
def list_review(place_id):
    """list of all Review objects by Place id"""
    if request.method == 'POST':
        return create_review(place_id)
    try:
        place = storage.get(Place, place_id)
    except Exception:
        abort(404)
    reviews = storage.all(Review)
    review_list = []
    for key, value in reviews.items():
        if place.id == value.to_dict().get('place_id'):
            review_list.append(value.to_dict())
    return jsonify(review_list)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review_by_id(review_id):
    """Retrieves a Review object by id"""
    try:
        place = storage.get(Review, review_id)
        review_dict = place.to_dict()
    except Exception:
        abort(404)
    return jsonify(review_dict)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """Deletes a Review_id by id"""
    try:
        review = storage.get(Review, review_id)
        storage.delete(review)
        storage.save()
        res = {}
    except Exception:
        abort(404)
    return jsonify(res), 200


def create_review(place_id):
    """Creates a Review"""
    try:
        place = storage.get(Place, place_id)
        if place is None:
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
    if 'text' not in name.keys() or name['text'] is None:
        abort(400, 'Missing text')
    n_review = {'text': name['text'], 'user_id': usr.id, 'place_id': place.id}
    review  = Review(**n_review)
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=["PUT"])
def update_review(review_id):
    """Updates a Review by id"""
    try:
        review = storage.get(Review, review_id)
    except Exception:
        abort(404)
    try:
        name = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')
    for key, value in name.items():
        if (key not in
                ('id', 'user_id', 'place_id', 'created_at', 'updated_at')):
            setattr(review, key, value)
        storage.save()
    return jsonify(review.to_dict()), 200
