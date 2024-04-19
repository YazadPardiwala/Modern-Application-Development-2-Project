from flask import Flask
from application.database import db
from application.config import LocalDevConfig, ProdConfig, Desired_config
from application.celery_system import make_celery
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_msearch import Search
from celery.schedules import crontab
import schedule, time

app = None
celery=None

def create_app():
    app = Flask(__name__)
    if Desired_config == 'PROD':
        print("starting production development")
        app.config.from_object(ProdConfig)
    elif Desired_config == 'DEV' :
        print("starting local development")
        app.config.from_object(LocalDevConfig)
    db.init_app(app)
    app.app_context().push()
    return app

app = create_app()

#initializing cors
CORS(app, resources={r"/*": {"origins": "http://localhost:9090"}})

#enabling m-search
search=Search()
search.init_app(app)

#initializing celery
#creating celery
celery=make_celery(app)


from application.controllers import *


if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 8000)

