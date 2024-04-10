from flask import Flask, current_app
from supabase import create_client, Client

supabase: Client = None


def init_app(app: Flask) -> None:
    with app.app_context():
        global supabase
        supabase = create_client(current_app.config["SUPABASE_URL"], current_app.config["SUPABASE_KEY"])
        supabase.auth.sign_in_with_password(
            {"email": current_app.config["SUPABASE_EMAIL"],
             "password": current_app.config["SUPABASE_PASSWORD"]}
        )
