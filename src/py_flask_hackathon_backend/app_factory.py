import os
from flask import Flask
from src.config import Config
from src.deps import fairy, blueprint, ma, db
from utils import import_name


def create_app(config=Config) -> Flask:
    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)
    ma.init_app(app)
    fairy.init_app(app)

    # Register blueprints
    blueprint.register_blueprints(app)

    # Register models
    for model in os.listdir("src/models"):
        if model != "__init__.py" and model.endswith(".py"):
            import_name("src.models", model.replace(".py", ""))

    @app.route("/")
    def hello_world():
        return "Hello, World!"

    return app
