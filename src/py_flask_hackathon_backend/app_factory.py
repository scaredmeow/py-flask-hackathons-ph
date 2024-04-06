from flask import Flask
from src.config import Config
from src.deps import fairy, blueprint, ma


def create_app(config=Config) -> Flask:
    app = Flask(__name__)

    app.config.from_object(config)

    # db.init_app(app)
    ma.init_app(app)
    fairy.init_app(app)
    blueprint.register_blueprints(app)

    @app.route("/")
    def hello_world():
        return "Hello, World!"

    return app
