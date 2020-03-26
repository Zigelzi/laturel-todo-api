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
        self.corect_projects = [{
            'name':'Test Project 1',
            'description': 'This is test project 1'
        },
        {
            'name':'Test Project 2',
            'description': 'This is test project 2'
        }]
        self.correct_project_json = json.dumps(self.correct_project)

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
        json_data = response.get_json()

        # Then
        self.assertEqual(json_data['status'], 'success')
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
        json_data = response.get_json()

        # Then
        self.assertEqual(json_data['status'], 'fail')
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
                        data=incorrect_description_project_json)
        json_data = response.get_json()

        # Then
        self.assertEqual(json_data['status'], 'fail')
        self.assertEqual(response.status_code, 401)

    def test_get_many_projects(self):
        # Given
        for project in self.corect_projects:
            self.add_project(project)
        
        # When
        response = self.app.get('/api/projects')
        json_data = response.get_json()

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['status'], 'success')
        self.assertTrue(isinstance(json_data['data']['projects'], list))
        self.assertEqual(len(json_data['data']['projects']), 2)
        

if __name__ == "__main__":
    unittest.main(exit=False)
    # Remove the SQLITE test db after tests have ran
    os.remove(f'{basedir}/tests/{test_db_name}')
    