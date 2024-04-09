import os

from dotenv import load_dotenv

load_dotenv(".env")

api_url_prefix: str = "/api/v1"


class Config:
    # ENV
    env_name = os.environ.get("ENV_NAME", "development")

    # APIFAIRY
    APIFAIRY_TITLE = os.environ.get("FAIRY_TITLE", "Hackathons PH")
    APIFAIRY_VERSION = os.environ.get("FAIRY_VERSION", "1.0")
    APIFAIRY_UI = os.environ.get("FAIRY_UI", "elements")
    APIFAIRY_UI_PATH = os.environ.get("FAIRY_UI_PATH", f"{api_url_prefix}/docs")

    # DATABASE
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///db.sqlite")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
