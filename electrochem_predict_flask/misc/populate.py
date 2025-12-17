from electrochem_predict_flask import app, db, Element, Ion, IonicComponent, IonicCompound

if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()

        elements = [
            ("Hydrogen", "H"),
            ("Helium", "He"),
            ("Lithium", "Li"),
            ("Sodium", "Na"),
            ("Potassium", "K"),
            ("Rubidium", "Rb"),
            ("Cesium", "Cs"),
            ("Francium", "Fr"),
            ("Beryllium", "Be"),
            ("Magnesium", "Mg"),
            ("Calcium", "Ca"),
            ("Strontium", "Sr"),
            ("Barium", "Ba"),
            ("Radium", "Ra"),
            ("Boron", "B"),
            ("Carbon", "C"),
            ("Nitrogen", "N"),
            ("Oxygen", "O"),
            ("Fluorine", "F"),
            ("Neon", "Ne"),
            ("Aluminum", "Al"),
            ("Silicon", "Si"),
            ("Phosphorus", "P"),
            ("Sulfur", "S"),
            ("Chlorine", "Cl"),
            ("Argon", "Ar"),
            ("Copper", "Cu"),
            ("Zinc", "Zn"),
            ("Iron", "Fe"),
            ("Nickel", "Ni"),
            ("Cobalt", "Co"),
            ("Yttrium", "Y"),
            ("Silver", "Ag"),
            ("Platinum", "Pt"),
            ("Gold", "Au"),
            ("Radon", "Rn"),
            ("Uranium", "U")
        ]

        for name, sign in elements:
            if not Element.query.filter_by(name=name).first():
                element = Element(name=name, sign=sign)
                db.session.add(element)

        db.session.commit()

        ions = [
            ("H", 1),
            ("OH", -1),
            ("Na", 1),
            ("Cl", -1),
            ("K", 1),
            ("Ca", 2),
            ("Mg", 2),
            ("NH4", 1)
        ]

        for name, charge in ions:
            if not Ion.query.filter_by(name=name).first():
                ion = Ion(name=name, charge=charge)
                db.session.add(ion)

        db.session.commit()