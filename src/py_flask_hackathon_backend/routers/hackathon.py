from flask import Blueprint

from apifairy import response
from src.schemas import HTTPRequestSchema

app = Blueprint("app", __name__)


@app.route("/")
@response(HTTPRequestSchema)
def index():
    return {"code": 200, "message": "Success", "description": "Hello, World!"}
