#!/usr/bin/python3
from flask import Flask, jsonify

app = Flask(__name__)

from models import storage
from api.v1.views import app_views

app.register_blueprint(app_views)
@app.teardown_appcontext
def close_db(Exception):
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """returns a JSON-formatted 404 status code response"""
    return jsonify({'error': 'not found'})

@app.errorhandler(400)
def request_body_error(error):
    """return json formatted 400 status coode"""
    return jsonify({'400': error.description})

port = 5000
host = '0.0.0.0'
if __name__ == "__main__":
    import os
    if os.getenv('HBNB_API_HOST'):
        host = os.getenv('HBNB_API_HOST')
    if os.getenv('HBNB_API_PORT'):
        port = os.getenv('HBNB_API_PORT')
    app.run(host=host, port=port, threaded=True)
