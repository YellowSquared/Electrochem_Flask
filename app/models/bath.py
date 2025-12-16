from typing import Optional
from .ion import Ion
from .ionic_compound import IonicCompound
from .electrode import Electrode
from app import db


class BathSoluteComponent(db.Model):
    bath_id = db.Column(db.Integer, db.ForeignKey("bath.id"), primary_key=True)
    ionic_compound_id = db.Column(db.Integer, db.ForeignKey(IonicCompound.id), primary_key=True)
    concentration = db.Column(db.Float, nullable=False)

    ionic_compound = db.relationship(IonicCompound, lazy=True)
    bath = db.relationship("Bath", lazy=True)


class Bath(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, default="Bath")
    solutes = db.relationship(BathSoluteComponent, back_populates="bath", lazy=True)
    anode_id = db.Column(db.Integer, db.ForeignKey(Electrode.id), nullable=False)
    cathode_id = db.Column(db.Integer, db.ForeignKey(Electrode.id), nullable=False)

    anode = db.relationship(Electrode, foreign_keys=[anode_id], lazy=True)
    cathode = db.relationship(Electrode, foreign_keys=[cathode_id], lazy=True)


    def dominating_anion(self) -> Optional[Ion]:
        anions = [
            solute for solute in self.solutes
            if solute.ionic_compound.anion
        ]
        sorted_anions = sorted(anions, key=lambda x: x.charge, reverse=True)
        return sorted_anions[0] if sorted_anions else None

    def dominating_cation(self) -> Optional[Ion]:
        cations = [
            solute for solute in self.solutes
            if solute.ionic_compound.cation
        ]
        sorted_cations = sorted(cations, key=lambda x: x.charge, reverse=True)
        return sorted_cations[0] if sorted_cations else None

