from flask import make_response, jsonify, request
import traceback
from api import app, db
from api.models import (
    Project, ProjectSchema,
    Task, TaskSchema
    )

# ---------------------------------
# Marshmallow serialization schemas
# ---------------------------------
project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

# Status message descriptions
status_msg_fail = 'fail'
status_msg_success = 'success'

@app.route('/api/project', methods=['POST'])
def add_project():
    response_object = {'status': status_msg_success}
    try:
        request_data = request.get_json()
        project = project_schema.load(request_data)
        project.save()
        db.session.commit()
        response_object['project'] = project_schema.dump(project)
        response_object['message'] = 'Project added succesfully!'
        json_response = jsonify(response_object)
        return make_response(json_response, 200)
    except Exception as e:
        response_object['status'] = status_msg_fail
        response_object['message'] = 'Something went wrong when trying to add project'
        db.session.rollback()
        json_response = jsonify(response_object)
        return make_response(json_response, 400)

@app.route('/api/project/<int:project_id>', methods=['GET'])
def get_project(project_id):
    response_object = {'status': status_msg_success}
    project = Project.query.get(project_id)
    try:
        if project:
            project_json = project_schema.dump(project)
            response_object['project'] = project_json
            response_object['message'] = 'Project queried successfully!'
            json_response = jsonify(response_object)
            return make_response(json_response, 200)
        elif project == None:
            response_object['status'] = status_msg_fail
            response_object['message'] = 'Queried project was not found'
            json_response = jsonify(response_object)
            return make_response(json_response, 404)
    except Exception as e:
        response_object['status'] = status_msg_fail
        response_object['message'] = 'Something went wrong when trying to fetch project'
        json_response = jsonify(response_object)
        return make_response(json_response, 400)

@app.route('/api/project/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    response_object = {'status': status_msg_success}
    project = Project.query.get(project_id)
    try:
        if project:
            project.delete()
            db.session.commit()
            response_object['message'] = 'Projects deleted succesfully!'
            json_response = jsonify(response_object)
            return make_response(json_response, 200)
        else:
            response_object['status'] = status_msg_fail
            response_object['message'] = 'Projects not found'
            return make_response(jsonify(response_object), 404)
    except Exception as e:
        response_object['status'] = status_msg_fail
        response_object['message'] = 'Something went wrong when trying to delete project'
        json_response = jsonify(response_object)
        return make_response(json_response, 400)

@app.route('/api/projects', methods=['GET'])
def get_all_projects():
    response_object = {'status': status_msg_success}
    try:
        all_projects = Project.get_all()
        all_projects_json = projects_schema.dump(all_projects)
        response_object['projects'] = all_projects_json
        response_object['message'] = 'Projects queried succesfully!'
        json_response = jsonify(response_object)
        return make_response(json_response, 200)
    except Exception as e:
        response_object['status'] = status_msg_fail
        response_object['message'] = 'Something went wrong when trying to fetch projects'
        json_response = jsonify(response_object)
        return make_response(json_response, 400)

@app.route('/api/task', methods=['POST'])
def add_task():
    response_object = {'status': status_msg_success}
    try:
        request_data = request.get_json()
        task = task_schema.load(request_data)
        task.save()
        db.session.commit()
        response_object['task'] = task_schema.dump(task)
        response_object['message'] = 'Task added successfully!'
        json_response = jsonify(response_object)
        return make_response(json_response, 200)
    except Exception as e:
        # traceback.print_exc()
        response_object['status'] = status_msg_fail
        response_object['message'] = 'Something went wrong when trying to add task'
        db.session.rollback()
        json_response = jsonify(response_object)
        return make_response(json_response, 400)

@app.route('/api/task/<int:task_id>', methods=['GET'])
def get_task(task_id):
    response_object = {'status': status_msg_success}
    task = Task.query.get(task_id)
    try:
        if task:
            task_json = task_schema.dump(task)
            response_object['task'] = task_json
            response_object['message'] = 'Task queried successfully!'
            json_response = jsonify(response_object)
            return make_response(json_response, 200)
        elif task == None:
            response_object['status'] = status_msg_fail
            response_object['message'] = 'Queried task was not found'
            json_response = jsonify(response_object)
            return make_response(json_response, 404)
    except Exception as e:
        response_object['status'] = status_msg_fail
        response_object['message'] = 'Something went wrong when trying to fetch task'
        json_response = jsonify(response_object)
        return make_response(json_response, 400)

@app.route('/api/task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    response_object = {'status': status_msg_success}
    task = Task.query.get(task_id)
    try:
        if task:
            task.delete()
            db.session.commit()
            response_object['message'] = 'Tasks deleted succesfully!'
            json_response = jsonify(response_object)
            return make_response(json_response, 200)
        else:
            response_object['status'] = status_msg_fail
            response_object['message'] = 'Task not found'
            return make_response(jsonify(response_object), 404)
    except Exception as e:
        response_object['status'] = status_msg_fail
        response_object['message'] = 'Something went wrong when trying to delete task'
        json_response = jsonify(response_object)
        return make_response(json_response, 400)

@app.route('/api/tasks', methods=['GET'])
def get_all_tasks():
    response_object = {'status': status_msg_success}
    try:
        all_tasks = Task.get_all()
        all_tasks_json = tasks_schema.dump(all_tasks)
        response_object['tasks'] = all_tasks_json
        response_object['message'] = 'Tasks queried succesfully!'
        json_response = jsonify(response_object)
        return make_response(json_response, 200)
    except Exception as e:
        response_object['status'] = status_msg_fail
        response_object['message'] = 'Something went wrong when trying to fetch tasks'
        json_response = jsonify(response_object)
        return make_response(json_response, 400)
