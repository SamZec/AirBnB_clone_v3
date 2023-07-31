#!/usr/bin/python3

import os
from flask import Flask, jsonify
from flask_cors import CORS

from models import storage
from api.v1.views import app_views



app = Flask(__name__)

""" Register the blueprint app_views to the Flask instance app """
app.register_blueprint(app_views)
app.url_map.strict_slashes = False
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


""" Method to handle teardown_appcontext """


@app.teardown_appcontext
def teardown_appcontext(exception):
    storage.close()


""" Handler for 404 errors """
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":

    """ Host and port configuration with fallback to default values """
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))

    app.run(host=host, port=port, threaded=True)
       
