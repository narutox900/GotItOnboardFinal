"""Flask configuration."""


class Config:
    """Base config."""
    SECRET_KEY = 'key'
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:p@localhost:33060/project'


class ProdConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    TESTING = False


class TestConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:p@localhost:33060/test'
