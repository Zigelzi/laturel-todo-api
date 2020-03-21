from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from api.config import DevConfig, Config

app = Flask(__name__)
app.config.from_object(DevConfig)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
# Flask-Marshmallow is used for serializing the DB objects to JSON.
ma = Marshmallow(app)

from api import routes, models