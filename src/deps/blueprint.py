from flask import Flask

from src.config import api_url_prefix


def register_blueprints(app: Flask):
    from src.deps import fairy_error
    from src.py_flask_hackathon_backend.routers import hackathon

    app.register_blueprint(fairy_error.errors)

    # Routers/Controllers

    # API
    app.register_blueprint(hackathon.app, url_prefix=f"{api_url_prefix}/hackathons")

    return app
