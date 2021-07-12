"""Flask configuration."""


class Config:
    """Base config."""
    SECRET_KEY = 'key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:p@localhost:33060/catalog_dev'


class ProductionConfig(Config):
    SECRET_KEY = 'production_key'


class DevelopmentConfig(Config):
    pass


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:p@localhost:33060/catalog_test'
