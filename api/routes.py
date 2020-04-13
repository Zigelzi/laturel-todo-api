from flask import make_response, jsonify, request
import traceback
from api import app, db
from api.models import (
    Project, ProjectSchema,
    Task, TaskSchema,
    User, UserSchema,
    Comment, CommentSchema
    )

# ---------------------------------
# Marshmallow serialization schemas
# ---------------------------------
project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

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
            if project.has_tasks():
                response_object['status'] = status_msg_fail
                response_object['message'] = 'Projects contains related tasks, unable to delete'
                json_response = jsonify(response_object)
                return make_response(json_response, 400)
            project.delete()
            db.session.commit()
            response_object['message'] = 'Project deleted succesfully!'
            json_response = jsonify(response_object)
            return make_response(json_response, 200)
        else:
            response_object['status'] = status_msg_fail
            response_object['message'] = 'Project not found'
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

@app.route('/api/task/add_assignee', methods=['POST'])
def add_assignee_to_task():
    response_object = {'status': status_msg_success}
    try:
        request_data = request.get_json()
        task = task_schema.load(request_data['task'])
        assignee = user_schema.load(request_data['user'])

        task = Task.query.get(task.id)
        assignee = User.query.get(assignee.id)
        if task:
            task_assignees = task.assignees.all()
            if assignee and (assignee in task_assignees):
                response_object['status'] = status_msg_fail
                response_object['message'] = 'Assignee already assigned to this task'
                json_response = jsonify(response_object)
                return make_response(json_response, 400)
            task.add_assignee(assignee)
            db.session.commit()
            response_object['task'] = task_schema.dump(task)
            response_object['message'] = 'Assignee added successfully!'
            json_response = jsonify(response_object)
            return make_response(json_response, 200)
        else:
            response_object['status'] = status_msg_fail
            response_object['message'] = 'Task that assignee was tried to be added to wasn\'t found'
            return make_response(jsonify(response_object), 404)
    except Exception as e:
        request_data = request.get_json()
        traceback.print_exc()
        print(request_data)
        response_object['status'] = status_msg_fail
        response_object['message'] = 'Something went wrong when trying to add assignee to task'
        json_response = jsonify(response_object)
        return make_response(json_response, 400)

@app.route('/api/task/remove_assignee', methods=['POST'])
def remove_assignee_from_task():
    response_object = {'status': status_msg_success}
    try:
        request_data = request.get_json()
        task = task_schema.load(request_data['task'])
        assignee = user_schema.load(request_data['user'])
        task = Task.query.get(task.id)
        if task:
            task.remove_assignee(assignee)
            db.session.commit()
            response_object['task'] = task_schema.dump(task)
            response_object['message'] = 'Assignee removed successfully!'
            json_response = jsonify(response_object)
            return make_response(json_response, 200)
        else:
            response_object['status'] = status_msg_fail
            response_object['message'] = 'Task that assignee was tried to be removed from wasn\'t found'
            return make_response(jsonify(response_object), 404)
    except Exception as e:
        traceback.print_exc()
        request_data = request.get_json()
        print(request_data)
        response_object['status'] = status_msg_fail
        response_object['message'] = 'Something went wrong when trying to remove assignee from task'
        json_response = jsonify(response_object)
        return make_response(json_response, 400)

@app.route('/api/user', methods=['POST'])
def add_user():
    response_object = {'status': status_msg_success}
    try:
        request_data = request.get_json()
        if request_data['name'] == '':
            response_object['status'] = status_msg_fail
            response_object['message'] = 'User name can\'t be empty'
            json_response = jsonify(response_object)
            return make_response(json_response, 400)
        user = user_schema.load(request_data)
        user.save()
        db.session.commit()
        response_object['user'] = user_schema.dump(user)
        response_object['message'] = 'User added succesfully!'
        json_response = jsonify(response_object)
        return make_response(json_response, 200)
    except Exception as e:
        response_object['status'] = status_msg_fail
        response_object['message'] = 'Something went wrong when trying to add user'
        db.session.rollback()
        json_response = jsonify(response_object)
        return make_response(json_response, 400)

@app.route('/api/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    response_object = {'status': status_msg_success}
    user = User.query.get(user_id)
    try:
        if user:
            user_json = user_schema.dump(user)
            response_object['user'] = user_json
            response_object['message'] = 'User queried successfully!'
            json_response = jsonify(response_object)
            return make_response(json_response, 200)
        elif user == None:
            response_object['status'] = status_msg_fail
            response_object['message'] = 'Queried user was not found'
            json_response = jsonify(response_object)
            return make_response(json_response, 404)
    except Exception as e:
        response_object['status'] = status_msg_fail
        response_object['message'] = 'Something went wrong when trying to fetch user'
        json_response = jsonify(response_object)
        return make_response(json_response, 400)

@app.route('/api/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    response_object = {'status': status_msg_success}
    user = User.query.get(user_id)
    try:
        if user:
            user.delete()
            db.session.commit()
            response_object['message'] = 'User deleted succesfully!'
            json_response = jsonify(response_object)
            return make_response(json_response, 200)
        else:
            response_object['status'] = status_msg_fail
            response_object['message'] = 'User not found'
            return make_response(jsonify(response_object), 404)
    except Exception as e:
        response_object['status'] = status_msg_fail
        response_object['message'] = 'Something went wrong when trying to delete user'
        json_response = jsonify(response_object)
        return make_response(json_response, 400)

@app.route('/api/users', methods=['GET'])
def get_all_user():
    response_object = {'status': status_msg_success}
    try:
        all_users = User.get_all()
        all_user_json = users_schema.dump(all_users)
        response_object['users'] = all_user_json
        response_object['message'] = 'Users queried succesfully!'
        json_response = jsonify(response_object)
        return make_response(json_response, 200)
    except Exception as e:
        response_object['status'] = status_msg_fail
        response_object['message'] = 'Something went wrong when trying to fetch user'
        json_response = jsonify(response_object)
        return make_response(json_response, 400)