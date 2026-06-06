import os
from flask import Flask
from .config import Config
from .extensions import db, login_manager

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'warning'

    # Register Blueprints
    from .routes import register_blueprints
    register_blueprints(app)

    # Create upload directories if they don't exist
    os.makedirs(app.config['UPLOAD_FOLDER_MATERIALS'], exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER_PYQS'], exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER_COMMUNITY'], exist_ok=True)

    return app
