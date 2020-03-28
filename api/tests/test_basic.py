import os
import unittest
import sys
import json

parent_dir = os.path.dirname
test_db_name = 'test.db'
# Add the package root directory to sys.path so imports work
sys.path.append(parent_dir(parent_dir(parent_dir(os.path.abspath(__file__)))))

from api import app, db
from api.config import basedir
from api.models import Project

json_header = {"Content-Type": "application/json"}

class TestCase(unittest.TestCase):
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

        db.drop_all()
        db.create_all()

    def add_project(self, project):
        project_json = json.dumps(project)
        response = self.app.post(
                        '/api/project',
                        headers=json_header,
                        data=project_json
                        )
        return response

    def tearDown(self):
        db.drop_all()
    
    def test_add_project_with_correct_data(self):
        # When
        response = self.add_project(self.correct_project)
        response_json_data = response.get_json()

        # Then
        self.assertEqual(response_json_data['status'], 'success')
        self.assertEqual(response_json_data['project']['name'], 'Test Project')
        self.assertEqual(response_json_data['project']['description'], 'This is test project')
        self.assertEqual(response_json_data['project']['id'], 1)
        self.assertEqual(response.status_code, 200)
    
    def test_add_project_with_incorrect_name(self):
        # Given
        incorrect_name_project = self.correct_project
        incorrect_name_project['name'] = 1
        incorrect_name_project_json = json.dumps(incorrect_name_project)

        # When 
        response = self.app.post(
                        '/api/project',
                        headers=json_header,
                        data=incorrect_name_project_json
                    )
        response_json_data = response.get_json()

        # Then
        self.assertEqual(response_json_data['status'], 'fail')
        self.assertEqual(response.status_code, 401)

    def test_add_project_with_incorrect_description(self):
        # Given
        incorrect_description_project = self.correct_project
        incorrect_description_project['description'] = 1
        incorrect_description_project_json = json.dumps(incorrect_description_project)

        # When 
        response = self.app.post(
                        '/api/project',
                        headers=json_header,
                        data=incorrect_description_project_json
                        )
        response_json_data = response.get_json()

        # Then
        self.assertEqual(response_json_data['status'], 'fail')
        self.assertEqual(response.status_code, 401)

    def test_get_many_projects(self):
        # Given
        for project in self.correct_projects:
            self.add_project(project)
        
        # When
        response = self.app.get('/api/projects')
        response_json_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json_data['status'], 'success')
        self.assertTrue(isinstance(response_json_data['projects'], list))
        self.assertEqual(len(response_json_data['projects']), 2)

    def test_delete_project_successfully(self):
        # Given
        add_project_response = self.add_project(self.correct_project)
        add_project_response_json_data = add_project_response.get_json()
        project = add_project_response_json_data['project']
        project_id = project['id']

        # When
        response = self.app.delete(
                        f'/api/project/{project_id}',
                        headers=json_header,
                        )
        response_json_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json_data['status'], 'success')

    def test_delete_non_existing_project(self):
        # Given
        project_id = 1

        # When
        response = self.app.delete(
                        f'/api/project/{project_id}',
                        headers=json_header,
                        )
        response_json_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_json_data['status'], 'fail')
        self.assertEqual(response_json_data['message'], 'Projects not found')

    def test_get_single_project_successfully(self):
        # Given there's existing project in database
        add_project_response = self.add_project(self.correct_project)
        add_project_response_json_data = add_project_response.get_json()
        project = add_project_response_json_data['project']
        project_id = project['id']

        # When that project is queried
        response = self.app.get(
                        f'/api/project/{project_id}',
                        headers=json_header
                        )
        response_json_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json_data['status'], 'success')
        self.assertEqual(response_json_data['message'], 'Project queried successfully!')
        self.assertEqual(response_json_data['project'], project)

    def test_get_non_existing_project(self):
        # Given there's nothing in the database and we query non-existing project
        project_id = 1

        # When the project is queried
        response = self.app.get(
                        f'/api/project/{project_id}',
                        headers=json_header
                        )
        response_json_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_json_data['status'], 'fail')
        self.assertEqual(response_json_data['message'], 'Queried project was not found')


if __name__ == "__main__":
    unittest.main(exit=False)
    # Remove the SQLITE test db after tests have ran
    os.remove(f'{basedir}/tests/{test_db_name}')
    