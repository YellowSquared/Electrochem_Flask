from typing import List, Optional
from .ion import Ion, IonRedoxReaction
from .ionic_compound import IonicCompound
from .electrode import Electrode

class BathTemp:
    def __init__(self, anode: Electrode, cathode: Electrode, solutes: List[IonicCompound]):
        self.anode = anode
        self.cathode = cathode
        self.solutes = solutes

    def dominating_reduction_reaction(self, n: int = 1) -> Optional[IonRedoxReaction]:
        reaction_potentials = self.get_cation_potentials_electrode_effect_applied()

        sorted_potentials = sorted(reaction_potentials.items(), key=lambda x: x[1], reverse=True)

        if 0 < n <= len(sorted_potentials):
            redox_id = sorted_potentials[n - 1][0]
            return IonRedoxReaction.query.get(redox_id)
        else:
            return None
        
    def dominating_oxidation_reaction(self, n: int = 1) -> Optional[IonRedoxReaction]:
        reaction_potentials = self.get_anion_potentials_electrode_effect_applied()

        sorted_potentials = sorted(reaction_potentials.items(), key=lambda x: x[1], reverse=False)

        if 0 < n <= len(sorted_potentials):
            redox_id = sorted_potentials[n - 1][0]
            return IonRedoxReaction.query.get(redox_id)
        else:
            return None


    def get_anion_potentials_electrode_effect_applied(self) -> dict[int, int]:
        anion_potentials = []
        for ionic_compound in self.solutes:
            anion_potentials.extend(ionic_compound.anion_component.ion.redox_potentials)

        return {
            potential.id: potential.potential + self.cathode.get_effect_on_redox(potential.id)
            for potential in anion_potentials
        }

    def get_cation_potentials_electrode_effect_applied(self) -> dict[int, int]:
        cation_potentials = []
        for ionic_compound in self.solutes:
            cation_potentials.extend(ionic_compound.cation_component.ion.redox_potentials)

        return {
            potential.id: potential.potential + self.anode.get_effect_on_redox(potential.id)
            for potential in cation_potentials
        }
