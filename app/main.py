from routes import main
from app import app


app.register_blueprint(main)

if __name__ == "__main__":
    app.run(debug=True)

