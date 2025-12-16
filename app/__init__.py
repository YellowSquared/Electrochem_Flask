from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
from app.models import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:4545@localhost:5432/temp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# with app.app_context():
#     db.create_all()


from .routes import main
app.register_blueprint(main)