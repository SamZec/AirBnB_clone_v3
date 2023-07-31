#!/usr/bin/python3
"""an endpoint that retrieves the number of each objects by type"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def status():
    """returns a JSON: "status": "OK" """
    return jsonify({'status': 'ok'})


@app_views.route("/stats")
def get_stats():
    """retrieves the number of each objects by type"""
    amenities = storage.count("Amenity")
    cities = storage.count("City")
    places = storage.count("Place")
    reviews = storage.count("Review")
    states = storage.count("State")
    users = storage.count("User")
    return jsonify({
        'amenities': amenities,
        'cities': cities,
        'places': places,
        'reviews': reviews,
        'states': states,
        'users': users
        })
