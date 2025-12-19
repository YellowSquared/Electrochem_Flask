from electrochem_predict_flask import db, Element, Ion, IonicCompound, IonElement, IonicComponent, create_app, \
    Electrode, IonRedoxReaction, IonRedoxResult, IonResult, CompoundResult, ElementResult, ElectrodeOverpotentialEffect, \
    Compound, CompoundElementComponent

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Create elements
        elements = [
            ("Aluminum", "Al"),
            ("Argon", "Ar"),
            ("Barium", "Ba"),
            ("Beryllium", "Be"),
            ("Boron", "B"),
            ("Bromine", "Br"),
            ("Calcium", "Ca"),
            ("Carbon", "C"),
            ("Chlorine", "Cl"),
            ("Copper", "Cu"),
            ("Cesium", "Cs"),
            ("Fluorine", "F"),
            ("Francium", "Fr"),
            ("Gold", "Au"),
            ("Helium", "He"),
            ("Hydrogen", "H"),
            ("Iron", "Fe"),
            ("Krypton", "Kr"),
            ("Lithium", "Li"),
            ("Magnesium", "Mg"),
            ("Manganese", "Mn"),
            ("Neon", "Ne"),
            ("Nickel", "Ni"),
            ("Nitrogen", "N"),
            ("Oxygen", "O"),
            ("Platinum", "Pt"),
            ("Potassium", "K"),
            ("Phosphorus", "P"),
            ("Radium", "Ra"),
            ("Radon", "Rn"),
            ("Rubidium", "Rb"),
            ("Silicon", "Si"),
            ("Sodium", "Na"),
            ("Strontium", "Sr"),
            ("Sulfur", "S"),
            ("Silver", "Ag"),
            ("Uranium", "U"),
            ("Yttrium", "Y"),
            ("Zinc", "Zn")
        ]

        # Add elements to the database
        for name, sign in elements:
            if not Element.query.filter_by(name=name).first():
                element = Element(name=name, sign=sign)
                db.session.add(element)

        db.session.commit()

        # Define ions and their corresponding charges
        ions = [
            ("Hydrogen", 1, [("Hydrogen", 1)]),  # Hydrogen Ion (H+)
            ("Hydroxide", -1, [("Oxygen", 1), ("Hydrogen", 1)]),  # Hydroxide (OH-)
            ("Sodium", 1, [("Sodium", 1)]),  # Sodium Ion (Na+)
            ("Chlorine", -1, [("Chlorine", 1)]),  # Chlorine Ion (Cl-)
            ("Potassium", 1, [("Potassium", 1)]),  # Potassium Ion (K+)
            ("Calcium", 2, [("Calcium", 1)]),  # Calcium Ion (Ca2+)
            ("Magnesium", 2, [("Magnesium", 1)]),  # Magnesium Ion (Mg2+)
            ("Ammonium", 1, [("Nitrogen", 1), ("Hydrogen", 4)]),  # Ammonium Ion (NH4+)
            ("Bromine", -1, [("Bromine", 1)]),  # Bromine Ion (Br-)
            ("Sulfate", -2, [("Sulfur", 1), ("Oxygen", 4)]),  # Sulfate Ion (SO4 2-)
            ("Nitrate", -1, [("Nitrogen", 1), ("Oxygen", 3)]),  # Nitrate Ion (NO3-)

            ("Lithium", 1, [("Lithium", 1)]),  # Lithium Ion (Li+)
            ("Iron", 3, [("Iron", 1)]),  # Iron(III) Ion (Fe3+)
            ("Zinc", 2, [("Zinc", 1)]),  # Zinc Ion (Zn2+)
            ("Copper", 2, [("Copper", 1)]),  # Copper(II) Ion (Cu2+)
            ("Silver", 1, [("Silver", 1)]),  # Silver Ion (Ag+)
            ("Aluminum", 3, [("Aluminum", 1)]),  # Aluminum Ion (Al3+)
            ("Phosphate", -3, [("Phosphorus", 1), ("Oxygen", 4)]),  # Phosphate Ion (PO4 3-)
            ("Carbonate", -2, [("Carbon", 1), ("Oxygen", 3)]),  # Carbonate Ion (CO3 2-)
            ("Hydrogen Sulfate", -1, [("Sulfur", 1), ("Oxygen", 4), ("Hydrogen", 1)]),  # Hydrogen Sulfate Ion (HSO4-)
            ("Hydrogen Phosphate", -2, [("Phosphorus", 1), ("Oxygen", 4), ("Hydrogen", 1)]) # Hydrogen Phosphate Ion (HPO4 2-)

        ]

        # Add ions and their associated IonElement entries
        for name, charge, elements in ions:
            ion = Ion.query.filter_by(name=name).first()
            if not ion:
                ion = Ion(name=name, charge=charge)
                db.session.add(ion)

                # Create IonElement relationships for each element in the ion
                for element_name, element_amount in elements:
                    element = Element.query.filter_by(name=element_name).first()
                    if element:
                        ion_element = IonElement(ion_id=ion.id, element_id=element.id, element_amount=element_amount)
                        db.session.add(ion_element)

        db.session.commit()

        compounds = [
            ("Water", (("Hydrogen", 2), ("Oxygen", 1)))
        ]

        for name, elements in compounds:
            comp = Compound(name=name)
            for element_name, amount in elements:
                element = CompoundElementComponent(compound_id=comp.id, element_id=Element.query.filter_by(
                    name=element_name).first().id, element_amount=amount)
                db.session.add(element)
            db.session.add(comp)

        db.session.commit()


        # Create IonicCompounds (e.g., Sodium Hydroxide, Magnesium Chloride)
        ionic_compounds = [
            ("Lithium Hydroxide", "Lithium", "Hydroxide"),  # Lithium Hydroxide (LiOH)
            ("Copper(II) Sulfate", "Copper", "Sulfate"),  # Copper(II) Sulfate (CuSO4)
            ("Zinc Chloride", "Zinc", "Chlorine"),  # Zinc Chloride (ZnCl2)
            ("Iron(III) Bromide", "Iron", "Bromine"),  # Iron(III) Bromide (FeBr3)
            ("Aluminum Phosphate", "Aluminum", "Phosphate"),  # Aluminum Phosphate (AlPO4)
            ("Silver Nitrate", "Silver", "Nitrate"),  # Silver Nitrate (AgNO3)
            ("Magnesium Carbonate", "Magnesium", "Carbonate"),  # Magnesium Carbonate (MgCO3)
            ("Calcium Phosphate", "Calcium", "Phosphate"),  # Calcium Phosphate (Ca3(PO4)2)
            ("Ammonium Carbonate", "Ammonium", "Carbonate"),  # Ammonium Carbonate (NH4)2CO3
            ("Potassium Phosphate", "Potassium", "Phosphate"),  # Potassium Phosphate (K3PO4)

            ("Sodium Hydroxide", "Sodium", "Hydroxide"),  # Sodium Hydroxide (NaOH)
            ("Potassium Hydroxide", "Potassium", "Hydroxide"),  # Potassium Hydroxide (KOH)
        ]

        for name, cation_name, anion_name in ionic_compounds:
            cation = Ion.query.filter_by(name=cation_name).first()
            anion = Ion.query.filter_by(name=anion_name).first()

            if cation and anion:
                # Create IonicComponent for cation and anion
                cation_component = IonicComponent(ion=cation, amount=1)
                anion_component = IonicComponent(ion=anion, amount=1)

                # Add the IonicComponents to the session
                db.session.add(cation_component)
                db.session.add(anion_component)

                # Create the IonicCompound
                ionic_compound = IonicCompound(name=name, cation_component=cation_component, anion_component=anion_component)
                db.session.add(ionic_compound)

        db.session.commit()

        electrodes = [
            "Graphite", "Boron doped diamond"
        ]

        for electrode in electrodes:
            db.session.add(Electrode(name=electrode))
        db.session.commit()

        redox_reactions = [
            (("Hydroxide", 4), (), ("Water", 2), ("Oxygen", 1), 0.4),
            (("Hydrogen", 2), (), (), ("Hydrogen", 2), 0)
            # Ion_name, (Ion result if any, amount) (Compound result if any, amount), (Element result if any, amount), potential
        ]

        reactions = []
        for ion, result_ion, result_compound, result_element, potential in redox_reactions:
            result = IonRedoxResult()
            redox = IonRedoxReaction(ion=Ion.query.filter_by(name=ion[0]).first(), potential=potential)
            reactions.append(redox)
            db.session.add(redox)

            # Handle Ion Result
            if result_ion:
                ion_result = IonResult(result_id=result.id, amount=result_ion[1],
                                       ion=Ion.query.filter_by(name=result_ion[0]).first())
                db.session.add(ion_result)

            # Handle Compound Result
            if result_compound:
                compound_result = CompoundResult(result_id=result.id, amount=result_compound[1],
                                                 compound=Compound.query.filter_by(name=result_compound[0]).first())
                db.session.add(compound_result)

            # Handle Element Result (if any)
            if result_element:
                element_result = ElementResult(result_id=result.id, amount=result_element[1],
                                               element=Element.query.filter_by(name=result_element[0]).first())
                db.session.add(element_result)

            result.redox = redox
            db.session.add(result)

        db.session.commit()

        e_effects = [
            ("Boron doped diamond", reactions[0], 0.5)
        ]

        for e_name, reaction, effect in e_effects:
            db.session.add(ElectrodeOverpotentialEffect(electrode=Electrode.query.filter_by(name=e_name).first(),
                                                        reaction=reaction,
                                                        overpotential_effect=effect
                                                        )
            )
        db.session.commit()





