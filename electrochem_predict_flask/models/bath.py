from typing import Optional
from .ion import Ion, IonRedoxReaction
from .ionic_compound import IonicCompound
from .electrode import Electrode, ElectrodeOverpotentialEffect
from electrochem_predict_flask import db


class BathSoluteComponent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bath_id = db.Column(db.Integer, db.ForeignKey("bath.id"))
    ionic_compound_id = db.Column(db.Integer, db.ForeignKey(IonicCompound.id), nullable=False)
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

    def dominating_reduction_(self) -> Optional[IonRedoxReaction]:
        anions = [
            solute.anion_component.ion_id for solute in self.solutes
        ]
        sorted_anions = sorted(anions, key=lambda x: x.charge, reverse=True)
        return sorted_anions[0] if sorted_anions else None

    def get_anion_potentials_electrode_effect_applied(self) -> dict[int, int]:
        anion_potentials: list[IonRedoxReaction] = [
            ionic_compound.anion_component.ion.potentials
            for ionic_compound in self.solutes.ionic_compound
        ]

        return {
            potential.id: potential.potential + self.cathode.get_effect_on_redox(potential.id)
            for potential in anion_potentials
        }

    def get_cation_potentials_electrode_effect_applied(self) -> dict[int, int]:
        cation_potentials: list[IonRedoxReaction] = [
            ionic_compound.cation_component.ion.potentials
            for ionic_compound in self.solutes.ionic_compound
        ]

        return {
            potential.id: potential.potential + self.anode.get_effect_on_redox(potential.id)
            for potential in cation_potentials
        }



