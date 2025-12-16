from flask_sqlalchemy import SQLAlchemy
from .ion import Ion
from app import db


class ElectrodeIonEffect(db.Model):
    electrode_id = db.Column(db.Integer, db.ForeignKey('electrode.id'), primary_key=True)
    ion_id = db.Column(db.Integer, db.ForeignKey(Ion.id), primary_key=True)
    overpotential_effect = db.Column(db.Float, nullable=True)

    electrode = db.relationship("Electrode", lazy=True)
    ion = db.relationship(Ion, lazy=True)


class Electrode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    material = db.Column(db.String(100), nullable=False)
    ion_overpotential_effect = db.relationship(ElectrodeIonEffect, lazy=True)



