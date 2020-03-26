from flask import make_response, jsonify, request
import traceback
from api import app, db
from api.models import Project, ProjectSchema

# ---------------------------------
# Marshmallow serialization schemas
# ---------------------------------
project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)

# Status message descriptions
status_msg_fail = 'fail'
status_msg_success = 'success'

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
    response_object = {'status': status_msg_success}
    try:
        request_data = request.get_json()
        project = project_schema.load(request_data)
        project.save()
        db.session.commit()
        response_object['data'] = project_schema.dump(project)
        response_object['message'] = 'Project added succesfully!'
        json_response = jsonify(response_object)
        return make_response(json_response, 200)
    except Exception as e:
        response_object['status'] = status_msg_fail
        response_object['message'] = 'Something went wrong when trying to add project'
        db.session.rollback()
        json_response = jsonify(response_object)
        return make_response(json_response, 401)

@app.route('/api/projects', methods=['GET'])
def get_all_projects():
    response_object = {'status': status_msg_success}
    try:
        all_projects = Project.query.all()
        all_projects_json = projects_schema.dump(all_projects)
        response_object['projects'] = all_projects_json
        response_object['message'] = 'Projects queried succesfully!'
        json_response = jsonify(response_object)
        return make_response(json_response, 200)
    except Exception as e:
        response_object['status'] = status_msg_fail
        response_object['message'] = 'Something went wrong when trying to fetch projects'
        json_response = jsonify(response_object)
        return make_response(json_response, 401)
