from electrochem_predict_flask import db

class Solubility(db.Model):
    ionic_compound_id = db.Column(db.Integer, db.ForeignKey("ionic_compound.id"), primary_key=True)
    solvent_id = db.Column(db.Integer, db.ForeignKey("ionic_solvent.id"), primary_key=True)
    value = db.Column(db.Float, nullable=False)

    solvent = db.relationship("IonicSolvent", lazy=True)
    ionic_compound = db.relationship("IonicCompound", lazy=True)