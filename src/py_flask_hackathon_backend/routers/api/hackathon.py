from apifairy import response, body
from flask import Blueprint, abort

from models.hackathons import Hackathon
from src.schemas import HackathonSchema, OKRequestSchema, UploadDocumentSchema
from src.decorators import paginated_response

app = Blueprint("app", __name__)


@app.route("/")
@paginated_response(schema=HackathonSchema(exclude=["upload"]))
def hackathons(data: dict):
    """Get all hackathons"""
    print(data)
    return Hackathon.query


@app.route("/<int:id>")
@response(HackathonSchema)
def hackathon(id):
    """Get hackathon by id"""
    return Hackathon.query.get_or_404(id)


@app.route("/", methods=["POST"])
@body(HackathonSchema(exclude=["id", 'upload']))
@response(OKRequestSchema)
def create_hackathon(data: dict):
    """Create a new hackathon"""
    try:
        hackathon = Hackathon(**data)
        hackathon.add_record()
    except Exception as e:
        abort(400, str(e))


@app.route("/<int:id>", methods=["PUT"])
@body(HackathonSchema(exclude=["id", 'upload']))
@response(OKRequestSchema)
def update_hackathon(data: dict, id: int):
    """Update hackathon by id"""
    try:
        hackathon = Hackathon.query.get_or_404(id)
        hackathon.update_record(**data)
    except Exception as e:
        abort(400, str(e))


@app.route("/<int:id>", methods=["DELETE"])
@response(OKRequestSchema)
def delete_hackathon(id: int):
    """Delete hackathon by id"""
    try:
        hackathon = Hackathon.query.get_or_404(id)
        hackathon.delete_record()
    except Exception as e:
        abort(400, str(e))


@app.route("/<int:id>/image", methods=["POST"])
@body(UploadDocumentSchema, location="form", media_type="multipart/form-data")
@response(OKRequestSchema)
def upload_image(data: dict, id: int):
    """Upload image for hackathon"""
    document = data.get("document")

    try:
        hackathon = Hackathon.query.get_or_404(id)
        hackathon.insert_image(document)
    except Exception as e:
        abort(400, str(e))
