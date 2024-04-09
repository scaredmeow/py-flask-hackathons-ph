from dataclasses import dataclass
from src.deps.db import db


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

    banner = db.relationship("Banner", back_populates="hackathon")
    content = db.relationship("Content", back_populates="hackathon")


@dataclass
class Banner(BaseModel):
    __tablename__ = "banners"

    hackathon_id = db.Column(db.Integer, db.ForeignKey("hackathons.id"), nullable=False)
    link = db.Column(db.String(100), nullable=False)

    hackathon = db.relationship("Hackathon", back_populates="banner")


@dataclass
class Content(BaseModel):
    __tablename__ = "contents"

    hackathon_id = db.Column(db.Integer, db.ForeignKey("hackathons.id"), nullable=False)
    description = db.Column(db.Text, nullable=False)

    hackathon = db.relationship("Hackathon", back_populates="contents")
