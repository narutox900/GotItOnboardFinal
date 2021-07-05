"""Flask configuration."""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base config."""
    SECRET_KEY = os.getenv('SECRET_KEY')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:12345678@localhost/project'


class ProdConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    TESTING = True
