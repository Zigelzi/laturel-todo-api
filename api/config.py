import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # Defult production config
    SECRET_KEY = os.getenv(f'SECRET_KEY', 'debugging')

    # Database settings
    SQLALCHEMY_DATABASE_URI = os.getenv(f'TODO_DATABASE_URL', 'sqlite:///')
    SQLALCHEMY_TRACK_MODIFICATIONS = False 

    # CORS
    CORS_HEADERS = 'Content-Type'

class DevConfig(Config):
    # Development config with debugging enabled
    DEBUG = True

    