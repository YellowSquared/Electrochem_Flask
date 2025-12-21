from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()
from .models import *

def create_app():
    load_dotenv()
    app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend/templates')

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    from .routes import main
    app.register_blueprint(main)

    db.init_app(app)
    migrate.init_app(app, db)

    return app