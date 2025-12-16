from flask_sqlalchemy import SQLAlchemy
from .compound import Compound
from app import db


class Solvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    compound_id = db.Column(db.Integer, db.ForeignKey(Compound.id), nullable=False)

    compound = db.relationship(Compound, lazy=True)
