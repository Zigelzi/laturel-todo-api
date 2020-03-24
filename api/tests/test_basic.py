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
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.drop_all()
    
    def test_add_project_with_correct_data(self):
        # Given
        project_json = json.dumps({
            'name':'Test Project',
            'description': 'This is test project'
        })

        # When
        response = self.app.post('/api/project', headers=json_header, data=project_json)
        response_json = response.get_json()

        # Then
        self.assertEqual(response_json['status'], 'success')
        self.assertEqual(response.status_code, 200)
    
    def test_add_project_with_incorrect_name(self):
        # Given
        project_json = json.dumps({
            'name': 1,
            'description': 'This is test project'
        })

        # When 
        response = self.app.post('/api/project', headers=json_header, data=project_json)
        response_json = response.get_json()

        # Then
        self.assertEqual(response_json['status'], 'fail')
        self.assertEqual(response.status_code, 401)

    def test_add_project_with_incorrect_description(self):
        # Given
        project_json = json.dumps({
            'name': 'Test Project',
            'description': 2
        })

        # When 
        response = self.app.post('/api/project', headers=json_header, data=project_json)
        response_json = response.get_json()

        # Then
        self.assertEqual(response_json['status'], 'fail')
        self.assertEqual(response.status_code, 401)

if __name__ == "__main__":
    unittest.main(exit=False)
    # Remove the SQLITE test db after tests have ran
    os.remove(f'{basedir}/tests/{test_db_name}')
    