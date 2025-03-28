# from app import create_app

# app = create_app()

# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def home():
        return "Hello, World!"

    return app