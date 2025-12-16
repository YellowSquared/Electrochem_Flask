from routes import main
from app import app, Element, db


app.register_blueprint(main)

if __name__ == "__main__":
    app.run(debug=True)



