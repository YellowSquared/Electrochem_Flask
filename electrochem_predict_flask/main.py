from electrochem_predict_flask import create_app, Element


def main():
    app = create_app()
    app.run(debug=True)

if __name__ == "__main__":
    main()
