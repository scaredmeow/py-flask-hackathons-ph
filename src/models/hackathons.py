from dataclasses import dataclass
from tempfile import NamedTemporaryFile
import uuid

from src.deps.db import db
from src.deps.supabase import supabase


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

    def add_record(self):
        db.session.add(self)
        db.session.commit()

    def delete_record(self):
        db.session.delete(self)
        db.session.commit()

    def update_record(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()


@dataclass
class Hackathon(BaseModel):
    __tablename__ = "hackathons"
    __table_args__ = {"extend_existing": True}

    title = db.Column(db.String(100), nullable=False)
    registration_end = db.Column(db.TIMESTAMP)
    date_from = db.Column(db.TIMESTAMP)
    date_end = db.Column(db.TIMESTAMP)
    prize_pool = db.Column(db.FLOAT)
    tags = db.Column(db.ARRAY(db.String), nullable=False)
    description = db.Column(db.Text)
    upload = db.Column(db.String(100))

    def __repr__(self):
        return self.title

    def get_image(self):
        return supabase.storage.from_("static").get_public_url(self.upload)

    def insert_image(self, document):
        document_uuid: str = str(uuid.uuid4())
        document_ext: str = document.filename.split(".")[-1]
        document_name: str = f"{document_uuid}.{document_ext}"

        self.upload = document_name
        self.update_record()

        temp = NamedTemporaryFile(delete=False)
        document.save(temp.name)

        with open(temp.name, "rb") as f:
            supabase.storage.from_("static").upload(
                file=f,
                path=self.upload,
                file_options={"content-type": "image/jpeg"}
            )
