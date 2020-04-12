import os
import unittest
import sys
import json
import datetime

parent_dir = os.path.dirname
test_db_name = 'test.db'
# Add the package root directory to sys.path so imports work
sys.path.append(parent_dir(parent_dir(parent_dir(os.path.abspath(__file__)))))

from api import app, db
from api.config import basedir
from api.models import Project

json_header = {"Content-Type": "application/json"}

class BaseTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{basedir}/tests/{test_db_name}'

        self.app = app.test_client()
        self.correct_project = {
            'name':'Test Project',
            'description': 'This is test project'
        }

        self.correct_projects = [{
            'name':'Test Project 1',
            'description': 'This is test project 1'
        },
        {
            'name':'Test Project 2',
            'description': 'This is test project 2'
        }]
        self.correct_task = {
            'name': 'Test task'
        }

        self.correct_tasks = [{
            'name':'Test Task 1'
        },
        {
            'name':'Test Task 2'
        }]

        self.correct_user = {
            'name': "Matti Meikäläinen"
        }

        self.correct_users = [
            {'name': 'Masa'},
            {'name': 'Erkki Esimerkki'}
        ]

        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.drop_all()

    def _set_key_to_number_999(self, data_key):
        incorrect_data = self.correct_project
        incorrect_data[data_key] = 999
        return incorrect_data

    def _add_user(self, user):
        user_json = json.dumps(user)
        response = self.app.post(
            '/api/user',
            headers=json_header,
            data=user_json
        )
        return response

    def _add_task(self, task):
        project_id = None
        if 'project_id' not in task:
            add_project_response_data = self._add_project_for_task()
            if 'project' in add_project_response_data:
                project_id = add_project_response_data['project']['id']
        else:
            project_id = task['project_id']
        
        task['project_id'] = project_id
        task_json = json.dumps(task)
        response = self.app.post(
            '/api/task',
            headers=json_header,
            data=task_json
        )
        return response

    def _add_project_for_task(self):
        project_json = json.dumps(self.correct_project)
        response = self.app.post(
            '/api/project',
            headers=json_header,
            data=project_json
        )
        response_data = response.get_json()
        return response_data


class TestProjects(BaseTest):
    def _add_project(self, project):
        project_json = json.dumps(project)
        response = self.app.post(
            '/api/project',
            headers=json_header,
            data=project_json
        )
        return response

    def _add_project_with_task(self):
        add_project_response = self._add_project(self.correct_project)
        add_project_response_data = add_project_response.get_json()
        project = add_project_response_data['project']

        task = {
            'name': 'Test task',
            'project_id': project['id']
        }
        add_task_response = self._add_task(task)
        return project

    def test_add_project_with_correct_data(self):
        # Given there's nothing in the database

        # When we add project with correct data
        response = self._add_project(self.correct_project)
        response_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status'], 'success')
        self.assertEqual(response_data['message'], 'Project added succesfully!')

        self.assertEqual(response_data['project']['id'], 1)
        self.assertEqual(response_data['project']['name'], 'Test Project')
        self.assertEqual(response_data['project']['description'], 'This is test project')
        self.assertEqual(response_data['project']['completed'], False)

        self.assertEqual(response_data['project']['updated_at'], None)
        self.assertEqual(response_data['project']['planned_complete_date'], None)
        self.assertEqual(response_data['project']['completed_at'], None)
    
    def test_add_project_with_incorrect_name(self):
        # Given we have project with incorrect type name
        incorrect_name_project = self._set_key_to_number_999('name')

        # When we try to add the incorrect data to database
        response = self._add_project(incorrect_name_project)
        response_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data['status'], 'fail')
        self.assertEqual(response_data['message'], 'Something went wrong when trying to add project')

    def test_add_project_with_incorrect_description(self):
        # Given we have project with incorrect type description
        incorrect_description_project = self._set_key_to_number_999('description')

        # When we try to add the incorrect data to database
        response = self._add_project(incorrect_description_project)
        response_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data['status'], 'fail')
        self.assertEqual(response_data['message'], 'Something went wrong when trying to add project')

    def test_add_project_with_no_name(self):
        # Given there is project in database and we have project with no name
        no_name_project = self.correct_project
        no_name_project['name'] = None

        # When new project with no name is added to empty database
        response = self._add_project(no_name_project)
        response_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data['status'], 'fail')
        self.assertEqual(response_data['message'], 'Something went wrong when trying to add project')

    def test_add_project_with_incorrect_completed(self):
        # Given there is project in database and we have project with incorrect name
        incorrect_completed_project = self._set_key_to_number_999('completed')

        # When new project with wrong type completed is submitted
        response = self._add_project(incorrect_completed_project)
        response_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data['status'], 'fail')
        self.assertEqual(response_data['message'], 'Something went wrong when trying to add project')

    def test_add_project_with_incorrect_created_at(self):
        # Given there is project in database and we have project with incorrect created_at
        incorrect_created_at_project = self._set_key_to_number_999('created_at')

        # When new project with wrong type completed is submitted
        response = self._add_project(incorrect_created_at_project)
        response_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data['status'], 'fail')
        self.assertEqual(response_data['message'], 'Something went wrong when trying to add project')

    def test_add_project_with_incorrect_updated_at(self):
        # Given there is project in database and we have project with incorrect updated_at
        incorrect_updated_at_project = self._set_key_to_number_999('updated_at')

        # When new project with wrong type completed is submitted
        response = self._add_project(incorrect_updated_at_project)
        response_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data['status'], 'fail')
        self.assertEqual(response_data['message'], 'Something went wrong when trying to add project')

    def test_add_project_with_incorrect_planned_complete_date(self):
        # Given there is project in database and we have project with incorrect planned_complete_date
        incorrect_planned_complete_date_project = self._set_key_to_number_999('planned_complete_date')

        # When new project with wrong type completed is submitted
        response = self._add_project(incorrect_planned_complete_date_project)
        response_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data['status'], 'fail')
        self.assertEqual(response_data['message'], 'Something went wrong when trying to add project')

    def test_add_project_with_incorrect_completed_at(self):
        # Given there is project in database and we have project with incorrect completed_at
        incorrect_completed_at_project = self._set_key_to_number_999('completed_at')

        # When new project with wrong type completed is submitted
        response = self._add_project(incorrect_completed_at_project)
        response_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data['status'], 'fail')
        self.assertEqual(response_data['message'], 'Something went wrong when trying to add project')    

    def test_get_many_projects(self):
        # Given there's multiple projects in database
        for project in self.correct_projects:
            self._add_project(project)
        
        # When we query all projects
        response = self.app.get('/api/projects')
        response_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status'], 'success')
        self.assertTrue(isinstance(response_data['projects'], list))
        self.assertEqual(len(response_data['projects']), 2)

    def test_delete_project_successfully(self):
        # Given we have one project in the database
        add_project_response = self._add_project(self.correct_project)
        add_project_response_data = add_project_response.get_json()

        project = add_project_response_data['project']
        project_id = project['id']

        # When we delete that same project from the database
        response = self.app.delete(
            f'/api/project/{project_id}',
            headers=json_header,
        )
        response_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status'], 'success')
        self.assertEqual(response_data['message'], 'Project deleted succesfully!')

    def test_delete_non_existing_project(self):
        # Given there's nothing in the database

        # When we delete non-existing project ID
        project_id = 1
        response = self.app.delete(
            f'/api/project/{project_id}',
            headers=json_header,
        )
        response_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data['status'], 'fail')
        self.assertEqual(response_data['message'], 'Project not found')

    def test_delete_project_with_tasks(self):
        # Given there's project with related task
        project = self._add_project_with_task()
        project_id = project['id']

        # When that project is attempted to be deleted
        response = self.app.delete(
            f'/api/project/{project_id}',
            headers=json_header
        )
        response_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data['status'], 'fail')
        self.assertEqual(response_data['message'], 'Projects contains related tasks, unable to delete')

    def test_get_single_project_successfully(self):
        # Given there's existing project in database
        add_project_response = self._add_project(self.correct_project)
        add_project_response_data = add_project_response.get_json()

        project = add_project_response_data['project']
        project_id = project['id']

        # When that project is queried
        response = self.app.get(
            f'/api/project/{project_id}',
            headers=json_header
        )
        response_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status'], 'success')
        self.assertEqual(response_data['message'], 'Project queried successfully!')
        self.assertEqual(response_data['project'], project)

    def test_get_non_existing_project(self):
        # Given there's nothing in the database and we query non-existing project
        project_id = 1

        # When the project is queried
        response = self.app.get(
            f'/api/project/{project_id}',
            headers=json_header
        )
        response_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data['status'], 'fail')
        self.assertEqual(response_data['message'], 'Queried project was not found')

class TestTasks(BaseTest):
    def _add_assignee_to_task(self, user, task):
        # Merging the two dictionaries together
        assignee_and_task = {
            'user': user,
            'task': task
        }
        assignee_and_task_json = json.dumps(assignee_and_task)    

        # When we add assignee to existing task
        response = self.app.post(
            f'/api/task/assignee',
            headers=json_header,
            data=assignee_and_task_json
        )
        return response

    def _remove_assignee_from_task(self, user, task):
        # Merging the two dictionaries together
        assignee_and_task = {
            'user': user,
            'task': task
        }
        assignee_and_task_json = json.dumps(assignee_and_task) 

        # When we add assignee to existing task
        response = self.app.delete(
            f'/api/task/assignee',
            headers=json_header,
            data=assignee_and_task_json
        )
        return response

    def test_add_task_with_correct_data(self):
        # Given there's project in database

        # When new task with correct data is added to empty database
        response = self._add_task(self.correct_task)
        response_data = response.get_json()
        project_id = response_data['task']['project_id']
        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status'], 'success')
        self.assertEqual(response_data['message'], 'Task added successfully!')
        self.assertEqual(response_data['task']['id'], 1)
        self.assertEqual(response_data['task']['name'], 'Test task')
        self.assertEqual(response_data['task']['completed'], False)

        self.assertEqual(response_data['task']['updated_at'], None)
        self.assertEqual(response_data['task']['planned_complete_date'], None)
        self.assertEqual(response_data['task']['planned_complete_date'], None)

        self.assertEqual(response_data['task']['project_id'], project_id)

    def test_add_task_without_project(self):
        # Given there's nothing in the database

        # When we try to add task without project_id foreign key
        task_without_project = self.correct_task
        task_without_project_json = json.dumps(task_without_project)
        response = self.app.post(
            '/api/task',
            headers=json_header,
            data=task_without_project_json
        )
        response_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data['status'], 'fail')
        self.assertEqual(response_data['message'], 'Something went wrong when trying to add task')

    def test_add_task_with_incorrect_name(self):
        # Given there is project in database and we have task with incorrect name
        incorrect_name_task = self._set_key_to_number_999('name')

        # When new task with wrong type name is submitted
        response = self._add_task(incorrect_name_task)
        response_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data['status'], 'fail')
        self.assertEqual(response_data['message'], 'Something went wrong when trying to add task')

    def test_add_task_with_no_name(self):
        # Given there is project in database and we have task with no name
        no_name_task = self.correct_task
        no_name_task['name'] = None

        # When new task with no name is added to empty database
        response = self._add_task(no_name_task)
        response_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data['status'], 'fail')
        self.assertEqual(response_data['message'], 'Something went wrong when trying to add task')

    def test_add_task_with_incorrect_completed(self):
        # Given there is project in database and we have task with incorrect name
        incorrect_completed_task = self._set_key_to_number_999('completed')

        # When new task with wrong type completed is submitted
        response = self._add_task(incorrect_completed_task)
        response_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data['status'], 'fail')
        self.assertEqual(response_data['message'], 'Something went wrong when trying to add task')

    def test_add_task_with_incorrect_created_at(self):
        # Given there is project in database and we have task with incorrect created_at
        incorrect_created_at_task = self._set_key_to_number_999('created_at')

        # When new task with wrong type completed is submitted
        response = self._add_task(incorrect_created_at_task)
        response_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data['status'], 'fail')
        self.assertEqual(response_data['message'], 'Something went wrong when trying to add task')

    def test_add_task_with_incorrect_updated_at(self):
        # Given there is project in database and we have task with incorrect updated_at
        incorrect_updated_at_task = self._set_key_to_number_999('updated_at')

        # When new task with wrong type completed is submitted
        response = self._add_task(incorrect_updated_at_task)
        response_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data['status'], 'fail')
        self.assertEqual(response_data['message'], 'Something went wrong when trying to add task')

    def test_add_task_with_incorrect_planned_complete_date(self):
        # Given there is project in database and we have task with incorrect planned_complete_date
        incorrect_planned_complete_date_task = self._set_key_to_number_999('planned_complete_date')

        # When new task with wrong type completed is submitted
        response = self._add_task(incorrect_planned_complete_date_task)
        response_data = response.get_json()
    
        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data['status'], 'fail')
        self.assertEqual(response_data['message'], 'Something went wrong when trying to add task')

    def test_add_task_with_incorrect_completed_at(self):
        # Given there is project in database and we have task with incorrect completed_at
        incorrect_completed_at_task = self._set_key_to_number_999('completed_at')

        # When new task with wrong type completed is submitted
        response = self._add_task(incorrect_completed_at_task)
        response_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data['status'], 'fail')
        self.assertEqual(response_data['message'], 'Something went wrong when trying to add task')

    def test_add_assignee_to_task(self):
        # Given there's existing user and task in the DB
        add_assignee_response = self._add_user(self.correct_user)
        add_assignee_response_data = add_assignee_response.get_json()
        assignee = add_assignee_response_data['user']
        
        add_task_response = self._add_task(self.correct_task)
        add_task_response_data = add_task_response.get_json()
        task = add_task_response_data['task']

        # When we add assignee to existing task
        response = self._add_assignee_to_task(assignee, task)
        response_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status'], 'success')
        self.assertEqual(response_data['message'], 'Assignee added successfully!')

        self.assertEqual(response_data['task']['id'], 1)
        self.assertEqual(response_data['task']['name'], 'Test task')
        self.assertEqual(response_data['task']['completed'], False)

        self.assertEqual(response_data['task']['updated_at'], None)
        self.assertEqual(response_data['task']['planned_complete_date'], None)
        self.assertEqual(response_data['task']['planned_complete_date'], None)

        self.assertTrue(isinstance(response_data['task']['assignees'], list))
        self.assertEqual(len(response_data['task']['assignees']), 1)
        self.assertEqual(response_data['task']['assignees'][0], assignee)

    def test_add_assignee_to_task_without_task(self):
        # Given there's existing user in the DB
        add_assignee_response = self._add_user(self.correct_user)
        add_assignee_response_data = add_assignee_response.get_json()
        assignee = add_assignee_response_data['user']

        task = {}

        # When we try to add assignee without task information
        response = self._add_assignee_to_task(assignee, task)
        response_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data['status'], 'fail')
        self.assertEqual(response_data['message'], 'Something went wrong when trying to add assignee to task')

    def test_add_assignee_to_task_without_assignee(self):
        # Given there's existing user in the DB
        assignee = {}

        add_task_response = self._add_task(self.correct_task)
        add_task_response_data = add_task_response.get_json()
        task = add_task_response_data['task']

        # When we try to add assignee without task information
        response = self._add_assignee_to_task(assignee, task)
        response_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data['status'], 'fail')
        self.assertEqual(response_data['message'], 'Something went wrong when trying to add assignee to task')

    def test_add_assignee_to_task_without_assignee_and_task(self):
        # Given there's existing user in the DB
        assignee = {}
        task = {}

        # When we try to add assignee without task information
        response = self._add_assignee_to_task(assignee, task)
        response_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data['status'], 'fail')
        self.assertEqual(response_data['message'], 'Something went wrong when trying to add assignee to task')

    def test_add_assignee_to_nonexisting_task(self):
        add_assignee_response = self._add_user(self.correct_user)
        add_assignee_response_data = add_assignee_response.get_json()
        assignee = add_assignee_response_data['user']
        
        add_task_response = self._add_task(self.correct_task)
        add_task_response_data = add_task_response.get_json()
        task = add_task_response_data['task']

        non_existing_task = task
        non_existing_task['id'] = 2

        # When we try to add assignee to task that doesn't exist
        response = self._add_assignee_to_task(assignee, non_existing_task)
        response_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data['status'], 'fail')
        self.assertEqual(response_data['message'], 'Task that assignee was tried to be added to wasn\'t found')

    def test_remove_assignee_from_task(self):
        # Given there's existing task with assignee
        add_assignee_response = self._add_user(self.correct_user)
        add_assignee_response_data = add_assignee_response.get_json()
        assignee = add_assignee_response_data['user']
        
        add_task_response = self._add_task(self.correct_task)
        add_task_response_data = add_task_response.get_json()
        task = add_task_response_data['task']

        add_assignee_response = self._add_assignee_to_task(assignee, task)
        add_assignee_response_data = add_assignee_response.get_json()
        task_with_assignee = add_assignee_response_data['task']

        # When we add assignee to existing task
        response = self._remove_assignee_from_task(assignee, task_with_assignee)
        response_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status'], 'success')
        self.assertEqual(response_data['message'], 'Assignee removed successfully!')

        self.assertEqual(response_data['task']['id'], 1)
        self.assertEqual(response_data['task']['name'], 'Test task')
        self.assertEqual(response_data['task']['completed'], False)

        self.assertEqual(response_data['task']['updated_at'], None)
        self.assertEqual(response_data['task']['planned_complete_date'], None)
        self.assertEqual(response_data['task']['planned_complete_date'], None)

        self.assertTrue(isinstance(response_data['task']['assignees'], list))
        self.assertEqual(len(response_data['task']['assignees']), 0)

    def test_remove_assignee_from_task_without_task(self):
        # Given there's existing task with assignee
        add_assignee_response = self._add_user(self.correct_user)
        add_assignee_response_data = add_assignee_response.get_json()
        assignee = add_assignee_response_data['user']
        
        add_task_response = self._add_task(self.correct_task)
        add_task_response_data = add_task_response.get_json()
        task = add_task_response_data['task']

        add_assignee_response = self._add_assignee_to_task(assignee, task)

        empty_task = {}

        # When we add assignee to existing task
        response = self._remove_assignee_from_task(assignee, empty_task)
        response_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data['status'], 'fail')
        self.assertEqual(response_data['message'], 'Something went wrong when trying to remove assignee from task')

    def test_remove_assignee_from_task_without_assignee(self):
        # Given there's existing task with assignee
        add_assignee_response = self._add_user(self.correct_user)
        add_assignee_response_data = add_assignee_response.get_json()
        assignee = add_assignee_response_data['user']
        
        add_task_response = self._add_task(self.correct_task)
        add_task_response_data = add_task_response.get_json()
        task = add_task_response_data['task']

        add_assignee_response = self._add_assignee_to_task(assignee, task)

        empty_assignee = {}

        # When we remove assignee to existing task
        response = self._remove_assignee_from_task(empty_assignee, task)
        response_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data['status'], 'fail')
        self.assertEqual(response_data['message'], 'Something went wrong when trying to remove assignee from task')

    def test_remove_assignee_from_task_without_assignee_and_task(self):
        # Given there's existing task with assignee
        add_assignee_response = self._add_user(self.correct_user)
        add_assignee_response_data = add_assignee_response.get_json()
        assignee = add_assignee_response_data['user']
        
        add_task_response = self._add_task(self.correct_task)
        add_task_response_data = add_task_response.get_json()
        task = add_task_response_data['task']

        add_assignee_response = self._add_assignee_to_task(assignee, task)

        empty_assignee = {}
        empty_task = {}

        # When we remove assignee to existing task
        response = self._remove_assignee_from_task(empty_assignee, empty_task)
        response_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data['status'], 'fail')
        self.assertEqual(response_data['message'], 'Something went wrong when trying to remove assignee from task')

    def test_remove_assignee_from_nonexisting_task(self):
        add_assignee_response = self._add_user(self.correct_user)
        add_assignee_response_data = add_assignee_response.get_json()
        assignee = add_assignee_response_data['user']
        
        add_task_response = self._add_task(self.correct_task)
        add_task_response_data = add_task_response.get_json()
        task = add_task_response_data['task']

        add_assignee_response = self._add_assignee_to_task(assignee, task)

        non_existing_task = task
        non_existing_task['id'] = 2

        # When we remove assignee to non existing task
        response = self._remove_assignee_from_task(assignee, non_existing_task)
        response_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data['status'], 'fail')
        self.assertEqual(response_data['message'], 'Task that assignee was tried to be removed from wasn\'t found')

    def test_get_many_tasks(self):
        # Given there's multiple projects in database
        for task in self.correct_tasks:
            self._add_task(task)
            
        # When we query all tasks
        response = self.app.get('/api/tasks')
        response_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status'], 'success')
        self.assertTrue(isinstance(response_data['tasks'], list))
        self.assertEqual(len(response_data['tasks']), 2)

    def test_delete_task_successfully(self):
        # Given we have one task in the database
        add_task_response = self._add_task(self.correct_task)
        add_task_response_data = add_task_response.get_json()

        task = add_task_response_data['task']
        task_id = task['id']

        # When we delete that same task from the database
        response = self.app.delete(
            f'/api/task/{task_id}',
            headers=json_header,
        )
        response_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status'], 'success')

    def test_delete_non_existing_task(self):
        # Given there's nothing in the database

        # When we delete non-existing task ID
        task_id = 1
        response = self.app.delete(
            f'/api/task/{task_id}',
            headers=json_header,
        )
        response_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data['status'], 'fail')
        self.assertEqual(response_data['message'], 'Task not found')

    def test_get_single_task_successfully(self):
        # Given there's existing task in database
        add_task_response = self._add_task(self.correct_task)
        add_task_response_data = add_task_response.get_json()

        task = add_task_response_data['task']
        task_id = task['id']

        # When that task is queried
        response = self.app.get(
            f'/api/task/{task_id}',
            headers=json_header
        )
        response_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status'], 'success')
        self.assertEqual(response_data['message'], 'Task queried successfully!')
        self.assertEqual(response_data['task'], task)

    def test_get_non_existing_task(self):
        # Given there's nothing in the database and we query non-existing task
        task_id = 1

        # When the task is queried
        response = self.app.get(
            f'/api/task/{task_id}',
            headers=json_header
        )
        response_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data['status'], 'fail')
        self.assertEqual(response_data['message'], 'Queried task was not found')
    
class TestUser(BaseTest):

    def _get_user(self, user_id):
        response = self.app.get(
            f'/api/user/{user_id}',
            headers=json_header
        )
        return response

    def test_add_user_with_correct_data(self):
        # Given there's nothing in the database

        # When we add user with correct data
        response = self._add_user(self.correct_user)
        response_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status'], 'success')
        self.assertEqual(response_data['message'], 'User added succesfully!')

        self.assertEqual(response_data['user']['id'], 1)
        self.assertEqual(response_data['user']['name'], 'Matti Meikäläinen')

    def test_add_user_incorrect_name(self):
        # Given we have user with incorrect type in name key
        incorrect_name_user = self._set_key_to_number_999('name')

        # When we try to add the incorrect data to database
        response = self._add_user(incorrect_name_user)
        response_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data['status'], 'fail')
        self.assertEqual(response_data['message'], 'Something went wrong when trying to add user')

    def test_add_user_with_no_name(self):
        # Given we have user with empty string as name
        no_name_user = self.correct_user
        no_name_user['name'] = ''

        # When we try to add the user to database
        response = self._add_user(no_name_user)
        response_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data['status'], 'fail')
        self.assertEqual(response_data['message'], 'User name can\'t be empty')


    def test_get_single_user_successfully(self):
        # Given there's existing user in the database
        add_user_response = self._add_user(self.correct_user)
        add_user_response_data = add_user_response.get_json()

        user = add_user_response_data['user']
        user_id = user['id']

        # When that user is queried
        response = self._get_user(user_id)
        response_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status'], 'success')
        self.assertEqual(response_data['message'], 'User queried successfully!')
        self.assertEqual(response_data['user'], user)

    def test_get_non_existing_user(self):
        # Given there's nothing in the database

        # When we query user id that doesn't exist
        user_id = 1
        response = self._get_user(user_id)
        response_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data['status'], 'fail')
        self.assertEqual(response_data['message'], 'Queried user was not found')

    def test_get_user_with_string_user_id(self):
        # Given there's existing user in the database
        self._add_user(self.correct_user)

        # When we query with invalid user_id
        user_id = 'asd'
        response = self._get_user(user_id)

        # Then
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.', response.data)

    def test_get_user_with_no_use1r_id(self):
        # Given there's existing user in the database
        self._add_user(self.correct_user)

        # When we query with invalid user_id
        user_id = ''
        response = self._get_user(user_id)

        # Then
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.', response.data)


    def test_get_many_users(self):
        # Given there's multiple projects in database
        for user in self.correct_users:
            res = self._add_user(user)
        
        # When we query all users
        response = self.app.get('/api/users')
        response_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status'], 'success')
        self.assertTrue(isinstance(response_data['users'], list))
        self.assertEqual(len(response_data['users']), 2)

    def test_delete_user_successfully(self):
        # Given we have one user in the database
        add_user_response = self._add_user(self.correct_user)
        add_user_response_data = add_user_response.get_json()

        user = add_user_response_data['user']
        user_id = user['id']

        # When we delete that same user from the database
        response = self.app.delete(
            f'/api/user/{user_id}',
            headers=json_header,
        )
        response_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status'], 'success')
        self.assertEqual(response_data['message'], 'User deleted succesfully!')


    def test_delete_non_existing_user(self):
        # Given there's nothing in the database

        # When we delete non-existing user ID
        user_id = 1
        response = self.app.delete(
            f'/api/user/{user_id}',
            headers=json_header,
        )
        response_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data['status'], 'fail')
        self.assertEqual(response_data['message'], 'User not found')

    
if __name__ == "__main__":
    unittest.main(exit=False)
    # Remove the SQLITE test db after tests have ran
    os.remove(f'{basedir}/tests/{test_db_name}')
    