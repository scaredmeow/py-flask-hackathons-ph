from dataclasses import dataclass

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

    def update_record(self):
        db.session.commit()


@dataclass
class Hackathon(BaseModel):
    __tablename__ = "hackathons"

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

    def insert_image(self, file_path):
        with open(file_path, "rb") as f:
            supabase.storage.from_("static").upload(
                file=f,
                path=self.upload,
                file_options={"content-type": "image/jpeg"}
            )
