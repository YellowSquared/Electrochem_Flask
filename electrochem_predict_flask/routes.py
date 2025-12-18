from flask import Blueprint

from electrochem_predict_flask import Element, Ion

main = Blueprint('main', __name__)

@main.route('/')
def index():
    sodium: Ion = Element.query.filter_by(sign="Na").first()
    sodium.sign = "Na2"
    return Element.query.filter_by(sign="Na").first().sign