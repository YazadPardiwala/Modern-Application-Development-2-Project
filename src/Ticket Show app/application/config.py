import os

basedir = os.path.abspath(os.path.dirname(__file__))

Desired_config = 'DEV'

class Config():
    DEBUG = False
    SQLITE_DB_DIR = basedir.removesuffix(r'\application')+r"\static\database"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(SQLITE_DB_DIR, r"DB.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = 'redis://localhost:6379/1',
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/2'

class LocalDevConfig(Config):
    DEBUG = True

class ProdConfig(Config):
    DEBUG = False