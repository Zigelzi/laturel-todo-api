from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from api.config import DevConfig, StageConfig, Config, todo_env

app = Flask(__name__)

if todo_env == 'development':
    print('Running in TODO development mode...')
    app.config.from_object(DevConfig)
elif todo_env == 'stage':
    print('Running in TODO staging mode...')
    app.config.from_object(StageConfig)
else:
    print('TODO environment was not found. Please review the configuration variables.')
    print (f'todo_env is {todo_env}')
    app.config.from_object(Config)

# Enable CORS for all resources
CORS(app, resources={r'/*': {'origins': '*'}})

db = SQLAlchemy(app)
migrate = Migrate(app, db)
# Flask-Marshmallow is used for serializing the DB objects to JSON.
ma = Marshmallow(app)

from api import routes, models