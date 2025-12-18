from typing import Optional

from .ion import Ion, IonRedoxReaction
from electrochem_predict_flask import db


class ElectrodeOverpotentialEffect(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    electrode_id = db.Column(db.Integer, db.ForeignKey('electrode.id'))
    reaction_id = db.Column(db.Integer, db.ForeignKey(IonRedoxReaction.id), nullable=False)
    overpotential_effect = db.Column(db.Float, nullable=False, default = 0)

    electrode = db.relationship("Electrode", lazy=True)
    reaction = db.relationship(IonRedoxReaction, lazy=True)


class Electrode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    material = db.Column(db.String(100), nullable=False)
    overpotential_effect = db.relationship(ElectrodeOverpotentialEffect, back_populates="electrode", lazy=True)

    def get_effect_on_redox(self, ion_redox_id: int) -> float:
        redox: Optional[ElectrodeOverpotentialEffect] = ElectrodeOverpotentialEffect.query.filter_by(
            electrode_id=self.id, reaction_id=ion_redox_id).first()
        if redox: return redox.overpotential_effect
        return 0
