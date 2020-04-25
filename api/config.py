import os

basedir = os.path.abspath(os.path.dirname(__file__))
todo_env = os.getenv('TODO_ENVIRONMENT')

class Config(object):
    # Defult production config
    SECRET_KEY = os.getenv(f'SECRET_KEY', 'debugging')

    # Database settings
    SQLALCHEMY_DATABASE_URI = os.getenv('sqlite:///')
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
    
    # CORS
    CORS_HEADERS = 'Content-Type'

class DevConfig(Config):
    # Development config with debugging enabled and using dev database
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(f'TODO_DATABASE_URL_DEV', 'sqlite:///')

class StageConfig(Config):
    # Stage config with debugging enabled and using stage database
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(f'TODO_DATABASE_URL_STAGE', 'sqlite:///')