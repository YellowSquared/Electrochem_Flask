from typing import Optional
from .ion import Ion
from .ionic_compound import IonicCompound
from .electrode import Electrode, ElectrodeIonEffect
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

    def get_anion_potentials_electrode_effect_applied(self) -> Optional[dict[int, float]]:
        anions: list[Ion] = [
            solute for solute in self.solutes
            if solute.ionic_compound.anion
        ]

        electrode_effect_dict = {effect.ion_id: effect for effect in self.cathode.ion_overpotential_effect}

        return {
            anion.id: anion.ion_potential + electrode_effect_dict.get(anion.id, 0.0)
            for anion in anions
        }

    def get_cation_potentials_electrode_effect_applied(self) -> Optional[dict[int, float]]:
        cations: list[Ion] = [
            solute for solute in self.solutes
            if solute.ionic_compound.cation
        ]

        electrode_effect_dict = {effect.ion_id: effect for effect in self.anode.ion_overpotential_effect}

        return {
            cation.id: cation.ion_potential + electrode_effect_dict.get(cation.id, 0.0)
            for cation in cations
        }



