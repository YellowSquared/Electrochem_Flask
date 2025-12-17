from flask_sqlalchemy import SQLAlchemy

from electrochem_predict_flask import db


class Element(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    sign = db.Column(db.String(10), unique=True, nullable=False)