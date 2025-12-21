from .ionic_compound import IonicCompound
from .compound import Compound
from electrochem_predict_flask import db


class IonicSolvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    compound_id = db.Column(db.Integer, db.ForeignKey(Compound.id), nullable=False)
    ionic_compund_id = db.Column(db.Integer, db.ForeignKey(IonicCompound.id), nullable=False)
    dissociation_rate = db.Column(db.Float, nullable=False, default=0)

    ionic_compound = db.relationship(IonicCompound, lazy=True)
    compound = db.relationship(Compound, lazy=True)
    
    def get_formula(self):
        return self.compound.get_formula()
    
    def __repr__(self):
        return self.get_formula()


