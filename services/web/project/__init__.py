import os
import datetime

from flask import Flask, Response, jsonify
from flask_sqlalchemy import SQLAlchemy

# instantiate the db
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)

    # register blueprints
    from project.api.bikeshare import bikeshare_blueprint
    app.register_blueprint(bikeshare_blueprint)

    # shell context for flask cli
    # registers the app and db to the shell
    app.shell_context_processor({'app': app, 'db': db})
    return app
