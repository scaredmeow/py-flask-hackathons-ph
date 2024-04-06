import os

from dotenv import load_dotenv

load_dotenv(".env")

api_url_prefix: str = "/api/v1"


class Config:
    # ENV
    env_name = os.environ.get("ENV_NAME", "development")
