import os
import unittest
import sys

# Add the package root directory to sys.path so imports work
parent_dir = os.path.dirname

# /home/miika/Projektit/laturel-todo/services/todo-api
sys.path.append(parent_dir(parent_dir(parent_dir(os.path.abspath(__file__)))))

from api import app, db
from api.config import basedir
from api.models import Project

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{basedir}/tests/test.db'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.drop_all()

    def test_get_project_page(self):
        response = self.app.get('/api/sanity')
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()