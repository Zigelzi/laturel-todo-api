from flask import make_response, jsonify

from api import app
from api.models import Project

@app.route('/api/sanity')
def index():
    response_object = {
        'status': 'success',
        'message': 'This is JSON from the backend!'
    }
    json_object = jsonify(response_object)
    return make_response(json_object, 200)

@app.route('/api/project', methods=['POST'])
def add_project():
    response_object = {'status': 'success'}
    json_object = jsonify(response_object)
    return make_response(json_object, 200)