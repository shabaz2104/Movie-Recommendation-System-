from flask import Flask

from config import Config
from routes import ui_blueprint


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(ui_blueprint)
    return app


if __name__ == "__main__":
    create_app().run(debug=True)
