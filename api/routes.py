from flask import make_response, jsonify
from api import app

@app.route('/')
def index():
    response_object = {
        'status': 'success',
        'message': 'testing'
    }
    json_object = jsonify(response_object)
    return make_response(json_object, 200)